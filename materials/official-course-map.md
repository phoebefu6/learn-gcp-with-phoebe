# learn-gcp-with-phoebe - official course map (source map)

GCP for Data & AI Teams, by Phoebe Fu. Two tracks: Leader a1-a6 (no account), Builder b1-b8 (BigQuery
sandbox + laptop). Built 2026-11-03. Every fact a page states lives here with its tier.

**Tiers.** `S` = read at source on 2026-11-03 (quote or number copied from the primary page).
`R` = reported (secondary source, or a primary page whose wording we could not read verbatim).
`C` = constructed (Tidewater Grocers and everything about it). `M` = modelled (our own model, labelled
on the page). Deeper quotes and URLs for every `S` line: `sources-gcp-docs.md` (same folder).

**Fast-moving product: re-verify the changelog before delivery.** Five renames landed in the last
eighteen months (below); prices, the sandbox limits and the free tier change without notice.

---

## 0. Decisions, palette, running case

- Palette (Phoebe-approved Google Cloud blue): primary `#1A73E8`, deep `#174EA6`, mid `#4285F4`,
  soft `#AECBFA`, 50-tint `#E8F0FE`, ink `#202124`, muted `#5F6368`, faint `#DADCE0`, hairline
  `#E8EAED`, warm `#FBBC04` (fill only, ink text), warm ink `#6B4A00`, warm tint `#FEF7E0`.
  Figure accents only: green `#188038` (5.0:1 on white), red `#C5221F` (5.8:1).
- Contrast checked before page 1: white on `#1A73E8` 4.51; white on `#174EA6` 7.85; `#1A73E8` text on
  `#E8F0FE` 3.93 FAILS, so every blue TEXT rule uses `#174EA6` (6.85 on the tint); ink on yellow 9.43;
  warm ink on yellow 4.72; muted on white 6.05, on tint 5.28.
- Nearest sibling `--indigo` (CIEDE2000, 180 siblings): learn-recommendation `#2563EB` 6.10,
  learn-python-data-analysis `#3776AB` 6.48, learn-automation `#0A64C4` 6.85. Below the estate's 10
  target; Phoebe's named hue overrides it (retheme-recipe rule). The brief's "known near sibling"
  `#1B72AB` is further than these three.
- Running case `C`: **Tidewater Grocers**, a constructed APAC grocery chain (Singapore, Malaysia,
  Indonesia). Organization `tidewater.example` (id 1001) > folders `data-platform`, `analytics`,
  `sandbox` > projects `tw-lake-prod` (data-platform), `tw-bi-prod` (analytics), `tw-lake-dev`
  (sandbox) > datasets `sales_raw`, `sales_curated`, `loyalty_pii` (prod) and `sales_curated` (dev);
  bucket `tw-lake-prod-landing`. Tag `1001/env` = prod/dev on projects, `1001/pii` = true on
  `loyalty_pii`. People: mei (analysts), raj (data-eng), ana (contractors), zoe (privacy-officers),
  sam (security), lin (loyalty lead), service account `ingest-pipeline@tw-lake-prod`.
- Session titles (grep 2026-11-03: AWS sibling already owns "Who can touch what", "The bill you did
  not plan", "A data platform on one page", "The IAM and cost bench"; ours differ):
  a1 What GCP is to a data team · a2 BigQuery is the warehouse and the lake · a3 Who gets in, at which
  level · a4 Pipelines without servers · a5 The bytes behind the bill · a6 Tidewater's platform on one
  page · b1 Cloud Storage layout and Parquet · b2 BigQuery in the sandbox · b3 Partitioning and
  clustering · b4 IAM as GCP evaluates it · b5 Dataflow and Beam, the idea · b6 Cloud Run or a
  function · b7 Vertex AI and BigQuery ML · b8 The GCP IAM and cost bench.

## 1. Seams (teach only our side; link the rest)

| Sibling | They own | We own |
|---|---|---|
| learn-aws-with-phoebe | AWS services | GCP; one AWS-to-GCP name table in a1 only |
| learn-terraform-with-phoebe | infrastructure as code (its session 4 shows `google_storage_bucket`) | console / gcloud / bq; link Terraform s4 for the code version |
| learn-data-warehouse, learn-databricks | warehouse modelling, lakehouse | what is specific to BigQuery |
| learn-data-access-control | RBAC/ABAC, row/column security concepts | IAM as GCP implements it; policy tags in one line |
| learn-data-engineering, learn-data-pipelines, learn-data-orchestration, learn-streaming-data | pipeline design | GCP service choice |
| learn-claude (session 68) | Claude on Vertex | the platform only |

URLs: https://phoebefu6.github.io/learn-aws-with-phoebe/ · https://phoebefu6.github.io/learn-terraform-with-phoebe/courses/04-modules-and-versions.html ·
https://phoebefu6.github.io/learn-data-warehouse-with-phoebe/ · https://phoebefu6.github.io/learn-databricks-with-phoebe/ ·
https://phoebefu6.github.io/learn-data-access-control-with-phoebe/ · https://phoebefu6.github.io/learn-data-engineering-with-phoebe/ ·
https://phoebefu6.github.io/learn-data-pipelines-with-phoebe/ · https://phoebefu6.github.io/learn-data-orchestration-with-phoebe/ ·
https://phoebefu6.github.io/learn-streaming-data-with-phoebe/ · https://phoebefu6.github.io/learn-claude-with-phoebe/courses/68-bedrock-vertex.html

## 2. Renames to state correctly (all `S`)

| Old name | Current name | Evidence |
|---|---|---|
| Cloud Functions | Cloud Run functions | Google Cloud blog, 22 August 2024 |
| Vertex AI | Gemini Enterprise Agent Platform ("Agent Platform"); Model Garden keeps its name | Agent Platform release notes, 22 April 2026 |
| Dataplex Universal Catalog | Knowledge Catalog ("API, client library, CLI, and IAM names remain unchanged") | Knowledge Catalog intro, 10 April 2026 |
| Dataproc / Dataproc Serverless | Managed Service for Apache Spark (gcloud still `gcloud dataproc`, `R`) | managed-spark docs banner; date not on page |
| Cloud Composer | "evolving to become Managed Service for Apache Airflow" | Composer overview; date not on page |
| Architecture Framework | Well-Architected Framework, six pillars | architecture/framework page |
| Cloud Skills Boost | skills.google (path 16, "Professional Data Engineer Certification") | 308 redirect observed |

Pages say "Vertex AI (now Gemini Enterprise Agent Platform)" on first use, because Phoebe's brief and
most learners still say Vertex AI.

## 3. Per-session coverage and facts

### a1 What GCP is to a data team (Leader, Foundations)
- `S` "The hierarchy consists of the organization (root) at the top, followed by folders (optional)
  for grouping, and then projects". "All resources except for the highest resource in a hierarchy
  have exactly one parent." A project is essential for "enabling billing, adding and removing
  collaborators, and managing permissions." (resource hierarchy page)
- `S` A Cloud Billing account "defines who pays for a given set of Google Cloud resources"; one billing
  account can be linked to several projects (billing concepts page).
- `S` "Regions are independent geographic areas that consist of zones"; a region has "three or more
  zones housed in three or more physical data centers". BigQuery multi-regions US and EU; Cloud
  Storage location types region, dual-region, multi-region (US, EU, ASIA). Singapore is
  asia-southeast1, Jakarta asia-southeast2, Kuala Lumpur asia-southeast4 (BigQuery pricing region list).
- `S` AWS-to-GCP name map (one table): S3 -> Cloud Storage; Athena + Redshift -> BigQuery; Glue ->
  Dataflow + Managed Service for Apache Spark (Dataproc) + Knowledge Catalog (Dataplex); Lambda ->
  Cloud Run functions; Bedrock -> Vertex AI (Agent Platform) Model Garden. Mapping is ours (`C`), the
  product names `S`.
- `S` Free Trial: "$300 Welcome credit to spend over 90 days"; "you must provide a credit card or
  other payment method". BigQuery sandbox: no card, no billing account.

### a2 BigQuery is the warehouse and the lake (Leader, Foundations)
- `S` On-demand: "you are charged for the number of bytes processed by each query"; capacity:
  "measured in slots (virtual CPUs) over time". Storage billed separately (active / long-term,
  logical / physical). => storage and compute billed separately.
- `S` "BigQuery uses a columnar data structure. You're charged according to the total data
  processed in the columns you select".
- `S` "External tables let you query structured data in external datastores." "BigLake tables let you
  query structured data in external datastores with access delegation." "you grant users access only
  to the BigLake table, not to the underlying datastore." BigLake formats: Avro, CSV, Delta Lake,
  Iceberg, JSON, ORC, Parquet.
- `S` Hive layout example "gs://my_bucket/my_table/dt=2019-10-31/lang=en/my_filename".
- `S` Long-term storage: not modified "for 90 consecutive days", price "drops by approximately 50%";
  "no difference in performance, durability, or availability".
- `C` team-shape argument (no cluster to size, so the platform team's work moves to cost and access).

### a3 Who gets in, at which level (Leader, Core)
- `S` "The effective allow policy for a resource is the union of the allow policy set at that resource
  and the allow policy inherited from its parent." "A specific access request to the resource is
  granted if any of the higher-level role bindings grant access to the request."
- `R` "There is no way to remove an inherited permission with an allow policy" is NOT a Google
  sentence; pages derive it from "union" + deny policies and say so.
- `S` Basic roles "include thousands of permissions across all Google Cloud services. In production
  environments, do not grant basic roles unless there is no alternative." New basic roles Admin /
  Writer / Reader; legacy Owner / Editor / Viewer. "you can't add conditions to role bindings for
  legacy basic roles." Predefined: "managed by Google Cloud services"; custom: "contain only the
  permissions that you specify".
- `S` Service account: "a special kind of account typically used by an application or compute
  workload"; "identified by its email address"; keys "are a security risk if not managed correctly".
- `S` Deny: "IAM always checks relevant deny policies before checking relevant allow policies."
  Attached to "an organization, folder, or project" and "inherited by all lower-level resources".
  Fields: denied principals, exception principals, denied permissions, exception permissions, denial
  condition ("only recognize resource tag functions"). Format "SERVICE_FQDN/RESOURCE.ACTION".
  Limit: up to 500 deny policies per resource, 500 deny rules in total.
- `S` IAM Conditions use CEL; examples `request.time < timestamp(...)`,
  `resource.name.startsWith('projects/_/buckets/...')`; "Only some resource types accept conditions".
- `S` Org Policy: IAM "focuses on who"; Organization Policy "focuses on what". Constraints
  `gcp.resourceLocations`, `iam.disableServiceAccountKeyCreation`, `storage.uniformBucketLevelAccess`.
- `S` BigQuery tags: tags can be used "to grant roles or deny access (Preview) through deny policies".

### a4 Pipelines without servers (Leader, Core)
- `S` "Dataflow is a Google Cloud service that provides unified stream and batch data processing at
  scale." "Dataflow executes Apache Beam pipelines." Billing units: worker vCPU and memory, Shuffle
  data processed, Streaming Engine; "billed in per second increments, on a per job basis".
- `S` Managed Service for Apache Spark (formerly Dataproc) clusters and serverless.
- `S` Pub/Sub: pull, push, BigQuery subscriptions; "By default, Pub/Sub offers at-least-once delivery
  with no ordering guarantees"; exactly-once on pull subscriptions only, same region.
- `S` Scheduled queries "use features of BigQuery Data Transfer Service". (5-minute minimum: `R`, not
  stated on pages.)
- `S` Composer named only ("evolving to become Managed Service for Apache Airflow").
- `S` Cloud Run: "your code can run as a service, job, worker pool, or instance"; request timeout
  default 5 minutes, up to 60 minutes; job tasks default 10 minutes, up to 168 hours.
- `C` the decision table by workload.

### a5 The bytes behind the bill (Leader, Applied)
- `S` On-demand "$6.25 / 1 tebibyte" (us-central1 default table), "The first 1 TiB of query data
  processed per month is free." "Charges are rounded up to the nearest MB, with a minimum 10 MB data
  processed per table referenced by the query, and with a minimum 10 MB data processed per query."
  "You aren't charged for queries that return an error or for queries that retrieve results from the
  cache." LIMIT does not reduce bytes ("even if you set an explicit LIMIT").
- `S` Editions: Standard, Enterprise, Enterprise Plus; pay-as-you-go per slot-hour in the default table
  Standard $0.04, Enterprise $0.06 (1-year $0.048, 3-year $0.036), Enterprise Plus $0.10; "Slots always
  autoscale to a multiple of 50"; baseline = minimum always allocated; billed per second with a
  one-minute minimum; commitments 1-year 20% / 3-year 40% discount (Enterprise, Enterprise Plus);
  Standard has "No access to BigQuery ML". Region for slot prices: default table (us-central1 first in
  the list); US multi-region not verified (`R`).
- `S` Storage (us-central1): active logical $0.000031507 per GiB-hour, long-term logical $0.000021918,
  active physical $0.000054795, long-term physical $0.000027397; first 10 GiB free each month; "For 1
  TiB for a full month, you pay $23.552" (active logical). Time travel and failsafe charges apply to
  physical storage.
- `S` "Cross-region load jobs are billed for network usage under Network Data Transfer SKUs."
- `S` Custom quotas: QueryUsagePerDay (project), QueryUsagePerUserPerDay; default project quota "200
  Tebibytes (TiB) of data processed per project per day". Maximum bytes billed: "the query fails
  without incurring a charge"; for clustered tables the estimate "is an upper bound", so a query can
  fail even though actual bytes would not exceed the limit.
- `S` Budgets: "Setting an alerts-only budget doesn't automatically cap ... spending." New spend-cap
  budgets: single project + single eligible service; eligible "Gemini API, Agent Platform (formerly
  known as Vertex AI), Cloud Run, and Cloud Run functions"; BigQuery not eligible. Launch stage
  Preview `R`.
- `S` 10 MB minimum per table (above). Every dollar on the page is from the bench's canon (section 4).

### a6 Tidewater's platform on one page (Leader, Capstone)
- `C` Tidewater reference architecture: landing bucket -> Cloud Run function -> BigQuery sales_raw ->
  scheduled SQL / Dataflow -> sales_curated -> BI project; loyalty_pii fenced by deny + tags; who owns
  each project.
- `S` Knowledge Catalog (formerly Dataplex): "unify technical metadata and business semantics";
  profiling scans check for "schema anomalies and statistical drift". Lakes/zones/assets are gone from
  current docs (`R`, legacy; not taught as current).
- `S` Column-level access with "policy tags"; role `datacatalog.categoryFineGrainedReader`; "enforced
  in addition to existing dataset ACLs". Row-level security: grantee list + filter expression that
  "functions like a WHERE clause". Concepts linked to learn-data-access-control.
- `S` Well-Architected Framework pillars: Operational excellence; Security, privacy, and compliance;
  Reliability; Cost optimization; Performance optimization; Sustainability.

### b1 Cloud Storage layout and Parquet (Builder, Foundations)
- `S` Storage classes: Standard (no minimum, no retrieval fee), Nearline 30 days, Coldline 90 days,
  Archive 365 days (all three "Retrieval fees: Yes"); the class table also lists a new zonal Rapid
  storage class (not taught);
  usage guidance once a month / once a quarter / less than once a year. Autoclass in one line.
- `S` Lifecycle: one action per rule (Delete, SetStorageClass, AbortIncompleteMultipartUpload);
  conditions incl. age, createdBefore, matchesPrefix, matchesStorageClass, numNewerVersions.
- `S` Uniform bucket-level access: ACLs disabled; "cannot be disabled after it has been active on a
  bucket for 90 consecutive days". Commands `gcloud storage buckets create gs://BUCKET/
  --uniform-bucket-level-access`, `gcloud storage cp`, `gcloud storage ls` (shown, need billing).
- `S` Free tier: "5 GB-months of regional storage (US regions only) per month" (Cloud Storage needs a
  billing account; shown as needs billing).
- RUN (pyarrow 25.0.1, Python 3.11.11): `buildalong/b1_layout.py` -> `outputs/b1_layout.txt`:
  18,362 rows; CSV 7,738,082 bytes; Parquet (snappy) 1,993,776 bytes; 11 year= partitions; a filter on
  year = 2019 opens 1 of 11 files; 1,800 rows in 2019.

### b2 BigQuery in the sandbox (Builder, Foundations)
- `S` Sandbox: "without providing a credit card or creating a billing account"; "lifetime limit of 10
  GiB of storage. This quota is not refunded upon data deletion"; 1 TiB query per month; tables,
  views, partitions "automatically expire after 60 days"; not supported: streaming, DML, Data Transfer
  Service. Public datasets in project `bigquery-public-data`.
- `S` Dry run: estimate "is an upper bound"; dry runs return 0 bytes on row-level-secured tables.
- `S` maximum bytes billed (a5).
- RUN (duckdb 2.0.0): `b2_sandbox_check.py` -> 2019 trips by payment type on the sample (Cash 872,
  Credit Card 871 ...). Sandbox numbers are "expected, your numbers will differ"; bytes estimate for the
  query = the bench model (three columns x 211,670,894 rows, see section 4), labelled modelled.

### b3 Partitioning and clustering (Builder, Core)
- `S` Partitioning: time-unit column, ingestion time (`_PARTITIONTIME`, hourly/daily/monthly/yearly),
  integer range (start, end, interval; example customer_id 0-100 step 10). require_partition_filter.
- `S` "Clustered tables in BigQuery sort data in storage blocks based on the values in user-defined
  clustered columns"; "the number of blocks to scan isn't known until a query runs, you don't receive
  an accurate cost estimate before execution". Clustering column order matters (`S`, clustered-tables page).
- RUN: `b3_ladder.py` (the cost engine) -> canon section 4.

### b4 IAM as GCP evaluates it (Builder, Core)
- `S` everything in a3, plus `gcloud projects get-iam-policy` output shape (shown, `R` format).
- RUN: `b4_iam.py` -> five Tidewater cases with trace (section 4).
- Policy tags in one line, link out.

### b5 Dataflow and Beam, the idea (Builder, Applied)
- `S` Beam: Pipeline, PCollection, PTransform, ParDo, GroupByKey, Combine; fixed, sliding, session,
  global windows; "Direct Runner ... executes pipelines on your machine", "not designed for production".
- RUN (apache-beam 2.77.0): `b5_beam.py` -> mean fare per year 2013 11.29 ... 2023 22.26 on the
  sample; 2019 trips per 30-day window [300, 150 x 9, 149]. The log shows Beam 2.77's DirectRunner
  handing the job to its local Prism runner. Dataflow runs shown as needs billing.

### b6 Cloud Run or a function (Builder, Applied)
- `S` renaming 22 August 2024; services vs jobs; timeouts (a4); functions-framework `pip install
  functions-framework`, `functions-framework --target ...`, port 8080; Pub/Sub trigger: direct
  (recommended) or Eventarc. Free tier: 2 million requests, 180,000 vCPU-seconds, 360,000 GiB-seconds
  per month (request-based billing, us-central1).
- RUN (functions-framework 3.10.2, Flask 3.1.3): `main.py` + curl -> accepted / rejected (HTTP 400),
  `outputs/b6_function.txt`. Docker is not installed on the build laptop: the Dockerfile is shown,
  not run.

### b7 Vertex AI and BigQuery ML (Builder, Applied)
- `S` CREATE MODEL variants and MODEL_TYPE list; ML.EVALUATE, ML.PREDICT; built-in model creation
  "$312.50 / 1 tebibyte" on demand; evaluation/prediction $6.25 per TiB inside the 1 TiB free tier;
  "BigQuery ML is available in Enterprise and Enterprise Plus Editions"; Standard has no BigQuery ML.
- `S` Free-tier table: "BigQuery ML models and training data stored in BigQuery are included in the
  BigQuery storage free tier" (pricing page).
- `S` BigQuery ML in the sandbox: NOT documented on the sandbox or pricing page. Pages say so and show
  CREATE MODEL as "needs a billing-enabled project, confirm in your own console".
- `S` Agent Platform (Vertex AI): Model Garden "discover, test, customize, and deploy models"; Claude
  models on Google Cloud via Model Garden; Workbench "Jupyter notebook-based".
- RUN (numpy 2.4.6): `b7_local_model.py` -> fare = 2.76 + 1.35 x miles + 0.43 x minutes; r2 0.883;
  MAE $2.31 on 2,995 held-out trips. Labelled "not BigQuery ML".

### b8 The GCP IAM and cost bench (Builder, Capstone)
- Section 4 canon, all from the engines in the browser.

## 4. Bench canon (python == node, by value; compare-canon.py exits 0; planted 0.1% fault exits 1)

### IAM resolver (assets/gcp-iam.js + gcp-iam-data.js; twin materials/iam_eval.py)
- 27 cases (25 requests + 2 binding validations) built from documented rules (doc line on each case).
- Correct logic: 27 of 27. Break "evaluate allow before deny": 24 of 27 (fails c06, c12, c21). Break
  "ignore inheritance": 13 of 27.
- Anti-lever (roles/editor on project tw-lake-prod for mei): c02 mei reads sales_raw.orders goes
  not-granted -> allow; mei's permissions on sales_curated.orders 27 -> 320 of the 334 modelled
  permissions; allowed requests in the table 10 -> 13; c26 (mei writes prod) stays deny.
- Basic-role contents are `M` (Viewer = read-only verbs get/list/getData/getMetadata/getIamPolicy;
  Editor = all modelled permissions except setIamPolicy; Owner = all). Role lists for the 8
  predefined roles are `S` (roles-2026-11-03.json).

### BigQuery cost meter (assets/gcp-cost.js + gcp-sample.js; twin materials/cost_ref.py)
Dataset: City of Chicago "Taxi Trips (2013-2023)" (wrvz-psew), BigQuery copy
`bigquery-public-data.chicago_taxi_trips.taxi_trips`. Licence: City of Chicago data portal Terms of
Use (not an open licence; use allowed, a derived application must carry the City's disclaimer, which
b1, b8 and the README do). Sample: 18,362 trips from 132 seeded 15-minute slots (seed 20261103).
Scale: 211,670,894 rows (portal column statistics) / 18,362 = 11,527.7. Column names and types are
BigQuery's (`R`, from public analyses of the table); logical sizes `S`.

| Rung | Columns | Rows read | Processed | Billed | On-demand |
|---|---|---|---|---|---|
| SELECT * | 23 | 211,670,894 | 82,705,058,760 B (77.03 GiB) | 78,874 MB | $0.4701 |
| three named columns, unpartitioned | 3 | 211,670,894 | 4,919,451,985 B (4.58 GiB) | 4,692 MB | $0.0280 |
| + day partitions, January 2019 | 3 | 1,213,529 | 28,203,678 B | 27 MB | $0.0002 |
| + cluster pickup_community_area = 56 (M) | 3 | 172,753 (36 of 257 blocks) | 4,014,960 B | 10 MB (minimum) | $0.0001 |

Monthly canon at 200 runs a day (the widget's default), 100 slots x 8 hours, Standard: SELECT * 451.32
TiB billed, $2,814.50 on demand; named columns 26.85 TiB, $161.55; partitioned 0.15 TiB, $0.00 (inside
the free TiB); clustered 0.06 TiB, $0.00; reservation $960.00 (Enterprise $1,440.00, Enterprise 1-year
$1,152.00). Per-row logical bytes, all 23 columns: 390.7 (taxi_id 130.0, unique_key 42.0,
pickup_location 34.3, dropoff_location 33.4, company 19.0, payment_type 9.0, fare 8.0).

January 2019 counts are exact portal counts per day and community area. Cluster model `M`: each day
partition sorted by pickup_community_area (NULLs first) into blocks of 5,000 rows. Monthly comparison
`M`: on-demand = billed x queries/day x 30, minus 1 TiB free, x $6.25; capacity = slots x hours/day x
30 x slot-hour price (assumes the reservation is billed for the hours set).

## 5. Professional Data Engineer exam mapping (`S`: exam guide PDF; $200, 2 hours, 40-50 questions)

| Section (weight) | Where | Not taught |
|---|---|---|
| 1 Designing data processing systems (~22%) | a1, a3, a6, b4 | data migrations (1.4) |
| 2 Ingesting and processing (~25%) | a4, b5, b6 | Composer DAGs, Datastream, CDC |
| 3 Storing the data (~20%) | a2, b1, b2, b3 | Bigtable, Spanner, AlloyDB, Cloud SQL |
| 4 Preparing and using data for analysis (~15%) | a2, b7 | Looker, BigQuery sharing (Analytics Hub) |
| 5 Maintaining and automating (~18%) | a5, b3, b8 | monitoring and alerting depth, Composer |

Official learning path: Google Cloud Skills Boost (now skills.google) path 16 "Professional Data
Engineer Certification". Certificates and labs stay official.

## 6. Not covered (honest list)

GKE; Spanner, Bigtable, AlloyDB beyond a name; Looker in depth; networking and VPC Service Controls
beyond one mention; Composer / Airflow; Dataform beyond a name; Gemini model training; principal access
boundary policies; IAM custom-role authoring; BigQuery Omni; real BigQuery block layout (modelled).

## 7. Citation appendix (all read 2026-11-03 unless marked)

- Resource hierarchy: https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy
- Geography and regions: https://docs.cloud.google.com/docs/geography-and-regions ; BigQuery locations https://docs.cloud.google.com/bigquery/docs/locations ; bucket locations https://docs.cloud.google.com/storage/docs/locations
- IAM overview https://docs.cloud.google.com/iam/docs/overview ; policy inheritance https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control ; roles overview https://docs.cloud.google.com/iam/docs/roles-overview ; roles reference https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery and /storage
- Deny policies https://docs.cloud.google.com/iam/docs/deny-overview ; supported permissions https://docs.cloud.google.com/iam/docs/deny-permissions-support
- IAM Conditions https://docs.cloud.google.com/iam/docs/conditions-overview ; BigQuery tags https://docs.cloud.google.com/bigquery/docs/tags
- Organization Policy https://docs.cloud.google.com/organization-policy/overview
- Service accounts https://docs.cloud.google.com/iam/docs/service-account-overview
- Cloud Storage classes https://docs.cloud.google.com/storage/docs/storage-classes ; lifecycle https://docs.cloud.google.com/storage/docs/lifecycle ; uniform access https://docs.cloud.google.com/storage/docs/uniform-bucket-level-access ; gcloud https://docs.cloud.google.com/storage/docs/discover-object-storage-gcloud
- Hive partitioned data https://docs.cloud.google.com/bigquery/docs/hive-partitioned-queries ; external sources https://docs.cloud.google.com/bigquery/docs/external-data-sources ; BigLake https://docs.cloud.google.com/bigquery/docs/biglake-intro
- BigQuery pricing https://cloud.google.com/bigquery/pricing ; data type sizes https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types#data_type_sizes ; estimate costs https://docs.cloud.google.com/bigquery/docs/estimate-costs ; best practices https://docs.cloud.google.com/bigquery/docs/best-practices-costs ; custom quotas https://docs.cloud.google.com/bigquery/docs/custom-quotas ; editions https://docs.cloud.google.com/bigquery/docs/editions-intro ; slots https://docs.cloud.google.com/bigquery/docs/slots
- Sandbox https://docs.cloud.google.com/bigquery/docs/sandbox ; partitioned tables https://docs.cloud.google.com/bigquery/docs/partitioned-tables ; clustered tables https://docs.cloud.google.com/bigquery/docs/clustered-tables
- Beam programming guide https://beam.apache.org/documentation/programming-guide/ ; Direct Runner https://beam.apache.org/documentation/runners/direct/ ; Dataflow https://docs.cloud.google.com/dataflow/docs/overview ; Dataflow pricing https://cloud.google.com/dataflow/pricing
- Managed Spark https://docs.cloud.google.com/managed-spark/docs/concepts/clusters-overview ; Pub/Sub https://docs.cloud.google.com/pubsub/docs/subscription-overview ; Composer https://docs.cloud.google.com/composer/docs/composer-3/composer-overview ; scheduled queries https://docs.cloud.google.com/bigquery/docs/scheduling-queries
- Cloud Run functions rename https://cloud.google.com/blog/products/serverless/google-cloud-functions-is-now-cloud-run-functions ; Cloud Run https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run ; timeouts https://docs.cloud.google.com/run/docs/configuring/request-timeout ; functions-framework https://github.com/GoogleCloudPlatform/functions-framework-python ; Pub/Sub triggers https://docs.cloud.google.com/run/docs/triggering/pubsub-triggers ; Cloud Run pricing https://cloud.google.com/run/pricing
- BigQuery ML CREATE MODEL https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create
- Agent Platform release notes https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes ; Model Garden https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-garden/explore-models ; Claude on Google Cloud https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude
- Knowledge Catalog https://docs.cloud.google.com/knowledge-catalog/docs/introduction ; column-level security https://docs.cloud.google.com/bigquery/docs/column-level-security-intro ; row-level security https://docs.cloud.google.com/bigquery/docs/row-level-security-intro
- Well-Architected Framework https://docs.cloud.google.com/architecture/framework
- Budgets https://docs.cloud.google.com/billing/docs/how-to/budgets ; spend caps https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps ; billing concepts https://docs.cloud.google.com/billing/docs/concepts ; free features https://docs.cloud.google.com/free/docs/free-cloud-features
- Professional Data Engineer https://cloud.google.com/learn/certification/data-engineer ; exam guide https://services.google.com/fh/files/misc/professional_data_engineer_exam_guide_english.pdf ; learning path https://www.skills.google/paths/16
- Chicago Taxi Trips (2013-2023) https://data.cityofchicago.org/Transportation/Taxi-Trips-2013-2023-/wrvz-psew ; Terms of Use https://www.chicago.gov/city/en/narr/foia/data_disclaimer.html
