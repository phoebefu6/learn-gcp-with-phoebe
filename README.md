<!-- learn-with-phoebe hub banner -->
> ### 📚 Part of [**Learn with Phoebe**](https://phoebefu6.github.io/learn-with-phoebe/)
> The shelf of 183 free, hands-on courses on AI, data, and the craft around them. **[Browse every course ↗](https://phoebefu6.github.io/learn-with-phoebe/)**
<!-- /learn-with-phoebe hub banner -->

# Learn GCP with Phoebe

**GCP for Data & AI Teams**, by Phoebe Fu. Fourteen 45-minute sessions in two tracks:

- **Leader track (6 sessions, no code, no account):** the resource hierarchy, BigQuery as warehouse and
  lake, IAM down the hierarchy, pipelines without servers, the bytes behind the bill, and one platform
  on a page, all on a constructed APAC grocery chain, Tidewater Grocers.
- **Builder track (8 sessions, BigQuery sandbox + a laptop):** Cloud Storage layout and Parquet, the
  BigQuery sandbox, partitioning and clustering, IAM as Google evaluates it, Apache Beam on the local
  runner, Cloud Run functions run locally with functions-framework, BigQuery ML and Vertex AI (now
  Gemini Enterprise Agent Platform), ending in a bench.

**The bench** (`courses/b8-the-gcp-iam-and-cost-bench.html`): an IAM evaluator following Google's
documented order (deny policies first, then allow policies unioned down the hierarchy), checked against
27 cases, with an Editor anti-lever and two break buttons; and a BigQuery on-demand bytes meter on real
Chicago taxi trips. Python twins of both engines live in `materials/` and agree with the browser to the
byte.

Static site: open `index.html`. No build step for the pages. Prices were read on 3 November 2026 and
change; re-verify before relying on them.

## Data notice

The taxi sample comes from the City of Chicago's Taxi Trips (2013-2023) dataset, used under the City
of Chicago data portal Terms of Use. This site provides applications using data that has been modified
for use from its original source, www.cityofchicago.org, the official website of the City of Chicago.
The City of Chicago makes no claims as to the content, accuracy, timeliness, or completeness of any of
the data provided at this site. The data provided at this site is subject to change at any time. It is
understood that the data provided at this site is being used at one's own risk.
