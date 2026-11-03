"""Python port of assets/gcp-iam.js: Google Cloud IAM evaluation for the Tidewater Grocers fixture.

Follows the documented order (read at source 2026-11-03):
  1. "IAM always checks relevant deny policies before checking relevant allow policies."
     Deny policies attach to an organization, folder or project and "are inherited by all
     lower-level resources". A deny rule applies when the principal is a denied principal and not
     an exception principal, the permission is denied and not an exception permission, and the
     denial condition (resource tag functions only) is true or absent.
  2. "The effective allow policy for a resource is the union of the allow policy set at that
     resource and the allow policy inherited from its parent." A binding grants when the principal
     matches, the role holds the permission, and its IAM Condition (CEL subset) is true.
  3. Anything else is not granted.
Role -> permission lists: the IAM roles reference pages for BigQuery and Cloud Storage, retrieved
2026-11-03 (materials/roles-2026-11-03.json). Legacy basic roles are MODELLED from their documented
definitions (Viewer = read-only actions, Editor = Viewer + state-changing actions, Owner = Editor +
managing roles), because Google lists their real thousands of permissions only in the console.
CEL subset: resource.name.startsWith('...'), request.time < / <= / > / >= timestamp('...'),
resource.matchTag('key', 'value'), !, &&, ||, parentheses. Anything else is refused.

Run: python iam_eval.py            -> prints every case verdict + the anti-lever and break numbers
     python iam_eval.py --json     -> the same as JSON (compared with node by compare-iam.py)
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = json.load(open(os.path.join(HERE, "iam-fixture.json")))
ROLES = {k: v for k, v in json.load(open(os.path.join(HERE, "roles-2026-11-03.json"))).items() if not k.startswith("_")}

FQDN = {"bigquery": "bigquery.googleapis.com", "storage": "storage.googleapis.com",
        "resourcemanager": "cloudresourcemanager.googleapis.com"}
READ_VERBS = {"get", "list", "getData", "getMetadata", "getIamPolicy"}


def universe():
    u = set()
    for perms in ROLES.values():
        u.update(perms)
    return sorted(u)


UNIVERSE = universe()


def verb(p):
    return p.split(".")[-1]


def role_perms(role):
    if role in ROLES:
        return set(ROLES[role])
    if role == "roles/viewer":
        return {p for p in UNIVERSE if verb(p) in READ_VERBS}
    if role == "roles/editor":
        return {p for p in UNIVERSE if verb(p) != "setIamPolicy"}
    if role == "roles/owner":
        return set(UNIVERSE)
    raise ValueError("unknown role " + role)


BASIC = {"roles/viewer", "roles/editor", "roles/owner"}

# ---------------- tiny CEL subset ----------------
TOK = re.compile(r"\s*(\|\||&&|<=|>=|<|>|!|\(|\)|,|\.|'[^']*'|[A-Za-z_][A-Za-z_0-9]*)")


def tokenize(s):
    out, i = [], 0
    s = s.strip()
    while i < len(s):
        m = TOK.match(s, i)
        if not m or m.end() == i:
            raise ValueError("unsupported CEL near: " + s[i:i + 20])
        out.append(m.group(1))
        i = m.end()
    return out


def cel(expr, ctx):
    toks = tokenize(expr)
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def take(t=None):
        x = peek()
        if t is not None and x != t:
            raise ValueError("unsupported CEL: expected %s got %s" % (t, x))
        pos[0] += 1
        return x

    def string():
        x = take()
        if not (x and x.startswith("'")):
            raise ValueError("unsupported CEL: expected string")
        return x[1:-1]

    def primary():
        x = peek()
        if x == "!":
            take(); return not primary()
        if x == "(":
            take(); v = orr(); take(")"); return v
        if x == "resource":
            take(); take(".")
            nm = take()
            if nm == "name":
                take("."); take("startsWith"); take("(")
                v = string(); take(")")
                return ctx["name"].startswith(v)
            if nm == "matchTag":
                take("("); k = string(); take(","); v = string(); take(")")
                return ctx["tags"].get(k) == v
            raise ValueError("unsupported CEL attribute resource." + nm)
        if x == "request":
            take(); take("."); take("time")
            op = take()
            if op not in ("<", "<=", ">", ">="):
                raise ValueError("unsupported CEL operator " + str(op))
            take("timestamp"); take("("); ts = string(); take(")")
            a, b = ctx["time"], ts
            return {"<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]
        raise ValueError("unsupported CEL token " + str(x))

    def andd():
        v = primary()
        while peek() == "&&":
            take(); w = primary(); v = v and w
        return v

    def orr():
        v = andd()
        while peek() == "||":
            take(); w = andd(); v = v or w
        return v

    v = orr()
    if peek() is not None:
        raise ValueError("unsupported CEL trailing " + str(peek()))
    return v


# ---------------- hierarchy ----------------
NODES = {n["id"]: n for n in FIX["nodes"]}


def ancestors(rid):
    """[resource, parent, ..., organization]"""
    out = []
    while rid:
        out.append(NODES[rid])
        rid = NODES[rid].get("parent")
    return out


def eff_tags(rid):
    tags = {}
    for n in reversed(ancestors(rid)):
        tags.update(n.get("tags", {}))
    return tags


def principals_of(p):
    s = {p, "principalSet://goog/public:all"}
    for g, members in FIX["groups"].items():
        if p in members:
            s.add(g)
    return s


def matches_perm(perm_fqdn, patterns):
    svc, rest = perm_fqdn.split("/", 1)
    res = rest.split(".")[0]
    for pat in patterns:
        if pat == perm_fqdn or pat == svc + "/*.*" or pat == svc + "/" + res + ".*":
            return True
    return False


def to_fqdn(perm):
    svc, rest = perm.split(".", 1)
    return FQDN.get(svc, svc + ".googleapis.com") + "/" + rest


def check_binding(b):
    if b.get("condition") and b["role"] in BASIC:
        return "You cannot use conditions when you grant legacy basic roles"
    return None


def evaluate(req, policies=None, mode="correct"):
    """req: principal, permission, resource, time. mode: correct | allow-first | no-inherit"""
    pol = policies or FIX
    chain = ancestors(req["resource"])
    if mode == "no-inherit":
        chain = chain[:1]
        if NODES[req["resource"]]["type"] not in ("organization", "folder", "project"):
            # deny policies live on org/folder/project; ignoring inheritance means only the
            # resource's own attachment point is read
            chain = [chain[0]]
    who = principals_of(req["principal"])
    ctx = {"name": NODES[req["resource"]]["name"], "tags": eff_tags(req["resource"]), "time": req["time"]}
    trace = []

    def deny_hit():
        pf = to_fqdn(req["permission"])
        for n in chain:
            for rule in pol["deny"].get(n["id"], []):
                if not (who & set(rule["deniedPrincipals"])):
                    continue
                if who & set(rule.get("exceptionPrincipals", [])):
                    trace.append("deny rule at %s: principal is an exception" % n["id"]); continue
                if not matches_perm(pf, rule["deniedPermissions"]):
                    continue
                if matches_perm(pf, rule.get("exceptionPermissions", [])):
                    trace.append("deny rule at %s: permission is an exception" % n["id"]); continue
                if rule.get("denialCondition") and not cel(rule["denialCondition"], ctx):
                    trace.append("deny rule at %s: denial condition false" % n["id"]); continue
                return n["id"], rule
        return None

    def allow_hit():
        for n in chain:
            for b in pol["allow"].get(n["id"], []):
                if not (who & set(b["members"])):
                    continue
                if req["permission"] not in role_perms(b["role"]):
                    continue
                if b.get("condition") and not cel(b["condition"], ctx):
                    trace.append("binding %s at %s: condition false" % (b["role"], n["id"])); continue
                return n["id"], b
        return None

    if mode == "allow-first":
        a = allow_hit()
        if a:
            return {"verdict": "allow", "step": "allow", "at": a[0], "role": a[1]["role"], "trace": trace}
    d = deny_hit()
    if d:
        return {"verdict": "deny", "step": "deny", "at": d[0], "trace": trace}
    a = allow_hit()
    if a:
        return {"verdict": "allow", "step": "allow", "at": a[0], "role": a[1]["role"], "trace": trace}
    return {"verdict": "not-granted", "step": "none", "trace": trace}


def with_antilever():
    pol = json.loads(json.dumps(FIX))
    pol["allow"].setdefault(FIX["antilever"]["at"], []).append(
        {"role": "roles/editor", "members": [FIX["antilever"]["member"]]})
    return pol


def held(principal, resource, pol=None):
    return sum(1 for p in UNIVERSE if evaluate(
        {"principal": principal, "permission": p, "resource": resource, "time": FIX["now"]}, pol)["verdict"] == "allow")


def run():
    cases = FIX["cases"]
    out = {"cases": [], "scores": {}, "antilever": {}}
    for mode in ("correct", "allow-first", "no-inherit"):
        ok = 0
        for c in cases:
            if c.get("kind") == "binding":
                got = "refused" if check_binding(c["binding"]) else "accepted"
            else:
                got = evaluate(c["request"], mode=mode)["verdict"]
            ok += got == c["expect"]
            if mode == "correct":
                out["cases"].append({"id": c["id"], "expect": c["expect"], "got": got})
        out["scores"][mode] = ok
    al = FIX["antilever"]
    pol = with_antilever()
    target = next(c for c in cases if c["id"] == al["case"])
    out["antilever"] = {
        "case": al["case"],
        "before": evaluate(target["request"])["verdict"],
        "after": evaluate(target["request"], pol)["verdict"],
        "held_before": held(al["member"], al["count_on"]),
        "held_after": held(al["member"], al["count_on"], pol),
        "universe": len(UNIVERSE),
        "allowed_cases_before": sum(1 for c in cases if c.get("kind") != "binding" and evaluate(c["request"])["verdict"] == "allow"),
        "allowed_cases_after": sum(1 for c in cases if c.get("kind") != "binding" and evaluate(c["request"], pol)["verdict"] == "allow"),
        "still_denied": evaluate(next(c for c in cases if c["id"] == al["holds"])["request"], pol)["verdict"],
    }
    return out


if __name__ == "__main__":
    r = run()
    if "--json" in sys.argv:
        print(json.dumps(r, indent=1, sort_keys=True))
    else:
        for c in r["cases"]:
            print("%-4s expect %-12s got %-12s %s" % (c["id"], c["expect"], c["got"], "" if c["expect"] == c["got"] else "MISMATCH"))
        print("scores", r["scores"], "of", len(r["cases"]))
        print("antilever", r["antilever"])
