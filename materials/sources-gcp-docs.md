# Sources - GCP docs (learn-gcp-with-phoebe)

Researched 2026-11-03. Quotes are verbatim and short. "read at source 2026-11-03" means the primary page was fetched that day.
"Last updated" is the date printed in the page footer (Google docs regenerate often, so most footers show late October 2026; treat it as a build date, not a content-change date).

Estate note: every `cloud.google.com/<product>/docs/...` URL now 301-redirects to `docs.cloud.google.com/<product>/docs/...`. Pricing pages stay on `cloud.google.com/<product>/pricing`. Several docs paths now redirect to renamed products (see sections 10, 13, 14).

---

## 1. Resource hierarchy

- Page: Resource hierarchy - https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy
- read at source 2026-11-03 | Last updated 2026-11-02
- "The hierarchy consists of the organization (root) at the top, followed by folders (optional) for grouping, and then projects"
- "All resources except for the highest resource in a hierarchy have exactly one parent."
- Project as base: "It is essential for creating, enabling, and using all Google Cloud services, managing APIs, enabling billing, adding and removing collaborators, and managing permissions."
- "You need a project resource to use Google Cloud."
- Inheritance: "Allow, deny, and organization policies are inherited through the hierarchy"
- "the effective policy for each resource in the hierarchy results from policies applied directly to the resource and policies inherited from its ancestors."

## 2. Locations

- Page: Geography and regions - https://docs.cloud.google.com/docs/geography-and-regions
- read at source 2026-11-03 | Last updated 2026-10-26
- "Regions are independent geographic areas that consist of zones."
- "A zone is a deployment area for Google Cloud resources within a region."
- Number: a region has "three or more zones housed in three or more physical data centers."
- Multi-region: "These multi-regional services are designed to be able to function following the loss of a single region."

- Page: BigQuery locations - https://docs.cloud.google.com/bigquery/docs/locations
- read at source 2026-11-03 | Last updated 2026-10-27
- "A region is a specific geographic place, such as London."
- US multi-region: "Data centers in the United States."
- EU multi-region: "Data centers within member states of the European Union."
- "multi-regions don't provide regional redundancy."
- Dataset location cannot change: only stated for BigQuery Omni ("After you create the dataset, the location cannot be changed."). General rule: NOT FOUND on page.

- Page: Bucket locations - https://docs.cloud.google.com/storage/docs/locations
- read at source 2026-11-03 | Last updated 2026-10-30
- "A region is a specific geographic place, such as Iowa (US-CENTRAL1)."
- "A dual-region is a specific pair of regions, such as Tokyo and Osaka (ASIA1)."
- "A multi-region is a large geographic area that contains two or more geographic regions."
- Multi-region names on page: US, EU, ASIA.

## 3. IAM overview, inheritance, roles, service accounts

- Page: IAM overview - https://docs.cloud.google.com/iam/docs/overview
- read at source 2026-11-03 | Last updated 2026-10-29
- "descendant resources effectively inherit their ancestor resources' allow policies."
- "The union of all of these policies is called the effective allow policy."
- Basic: "Highly permissive roles that provide broad access to Google Cloud services."
- Predefined: "Roles that are managed by Google Cloud services."
- Custom: "Roles that you create that contain only the permissions that you specify."
- Against basic roles in prod: "These roles can be useful for testing purposes, but shouldn't be used in production environments."

- Page: Policy inheritance - https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control
- read at source 2026-11-03 | Last updated 2026-10-29
- "The effective allow policy for a resource is the union of the allow policy set at that resource and the allow policy inherited from its parent."
- "No way to remove an inherited permission with an allow policy": NOT FOUND on page (nor on the IAM overview, allow-policies or hierarchy pages). Only secondary sources state it (e.g. https://open-exam-prep.com/study-guides/gcp-ace/iam-policies-and-role-types/iam-policies-structure-bindings-hierarchy). Safe course wording: derive it from "union" plus the deny-policy section below.

- Page: Allow policies - https://docs.cloud.google.com/iam/docs/allow-policies
- read at source 2026-11-03
- "A specific access request to the resource is granted if any of the higher-level role bindings grant access to the request."

- Page: Service accounts overview - https://docs.cloud.google.com/iam/docs/service-account-overview
- read at source 2026-11-03 | Last updated 2026-10-29
- "A service account is a special kind of account typically used by an application or compute workload, such as a Compute Engine instance, rather than a person."
- "A service account is identified by its email address"
- Keys: "Service account keys are a security risk if not managed correctly."
- "You should choose a more secure alternative to service account keys whenever possible."

- Page: Service account impersonation - https://docs.cloud.google.com/iam/docs/service-account-impersonation
- read at source 2026-11-03
- "authenticates as a service account to gain the service account's permissions, it's called impersonating the service account."
- "Impersonation is useful when you want to change a user's permissions without changing your Identity and Access Management (IAM) policies."

## 4. IAM deny policies

- Page: Deny policies - https://docs.cloud.google.com/iam/docs/deny-overview
- read at source 2026-11-03 | Last updated 2026-10-29
- "IAM always checks relevant deny policies before checking relevant allow policies."
- "Each deny policy is attached to an organization, folder, or project."
- Denied principals: "The principals that are denied permissions."
- Exception principals: "The principals that are exempt from the deny rule."
- Denied permissions: "The permissions that the specified principals are unable to use, or denied."
- Exception permissions: "A list of permissions that the specified principals can use, even if those permissions are included in" the denied permissions.
- Denial condition: "A logic expression that affects when the deny rule applies."
- Permission format: "SERVICE_FQDN/RESOURCE.ACTION"; page example is iam.googleapis.com/roles.delete. The BigQuery example bigquery.googleapis.com/tables.getData: NOT FOUND on page (it follows the stated format, but quote the iam example).
- Wildcards: "SERVICE_FQDN/*.* : Denies all permissions for the specified service."
- Limits: "Each resource can have up to 500 deny policies." and "Together, these deny policies can contain a total of 500 deny rules."

## 5. IAM Conditions

- Page: Overview of IAM Conditions - https://docs.cloud.google.com/iam/docs/conditions-overview
- read at source 2026-11-03 | Last updated 2026-10-29
- "Common Expression Language, or CEL, is the expression language used to specify an expression in IAM Conditions."
- Attribute examples: "request.time < timestamp('2021-01-01T00:00:00Z')" and "resource.name.startsWith('projects/_/buckets/exampleco-site-assets/')"
- Supported types: "Only some resource types accept conditions in role bindings."
- Basic roles (VERIFIED): "You cannot use conditions when you grant legacy basic roles, including Owner (roles/owner), Editor (roles/editor), and Viewer (roles/viewer)."
- Also not with allUsers / allAuthenticatedUsers (same note).
- Cloud Storage: conditions on a bucket allow policy need uniform bucket-level access enabled.
- Limit: "As a best practice, don't add more than 100 conditional role bindings to a single allow policy."

## 6. Organization Policy Service

- Page: Introduction to the Organization Policy Service - https://docs.cloud.google.com/organization-policy/overview (old resource-manager path redirects here)
- read at source 2026-11-03 | Last updated 2026-10-26
- "Identity and Access Management focuses on who, and lets the administrator authorize who can take action on specific resources based on permissions."
- "Organization Policy focuses on what, and lets the administrator set restrictions on specific resources to determine how they can be configured."
- "A constraint is a particular type of restriction against a Google Cloud service or a list of Google Cloud services."

- Page: Organization policy constraints list - https://docs.cloud.google.com/organization-policy/reference/org-policy-constraints
- read at source 2026-11-03 | Last updated 2026-10-26
- gcp.resourceLocations: "This list constraint defines the set of locations where location-based Google Cloud resources can be created."
- iam.disableServiceAccountKeyCreation: "This boolean constraint, when enforced, disables the creation of service account external keys and Cloud Storage HMAC keys."
- Newer managed variant also listed: constraints/iam.managed.disableServiceAccountKeyCreation - "This constraint, when enforced, blocks service account key creation."
- storage.uniformBucketLevelAccess: "This boolean constraint requires buckets to use uniform bucket-level access where this constraint is set to True."
- iam.allowedPolicyMemberDomains (Domain restricted sharing): "This list constraint defines the organization principal sets and Google Workspace customer IDs" (whose principals may be added to IAM policies).

## 7. Cloud Storage

- Page: Storage classes - https://docs.cloud.google.com/storage/docs/storage-classes
- read at source 2026-11-03 | Last updated 2026-10-30
- Minimum durations from the class table: Standard none, "NEARLINE 30 days", "COLDLINE 90 days", "ARCHIVE 365 days".
- "Nearline storage is ideal for data you plan to read or modify on average once per month or less."
- "Coldline storage is ideal for data you plan to read or modify at most once a quarter."
- "Archive storage is the best choice for data that you plan to access less than once a year."
- Autoclass: "You can enable the Autoclass feature on a bucket to let Cloud Storage manage storage class transitions for you automatically."

- Page: Object Lifecycle Management - https://docs.cloud.google.com/storage/docs/lifecycle
- read at source 2026-11-03 | Last updated 2026-10-30
- "A lifecycle rule specifies exactly one of the following actions:" Delete, SetStorageClass, AbortIncompleteMultipartUpload.
- "Lifecycle rules support the following conditions:" age, createdBefore, customTimeBefore, daysSinceCustomTime, daysSinceNoncurrentTime, isLive, matchesStorageClass, matchesPrefix / matchesSuffix, noncurrentTimeBefore, numNewerVersions, sizeAboveBytes / sizeBelowBytes.
- Limit: "You can have up to 1000 prefixes and suffixes in total specified across all rules." Max rules per bucket: NOT FOUND on page.

- Page: Uniform bucket-level access - https://docs.cloud.google.com/storage/docs/uniform-bucket-level-access
- read at source 2026-11-03 | Last updated 2026-10-30
- "Access Control Lists (ACLs) are disabled, and only bucket-level" IAM permissions grant access.
- "Generally, using uniform bucket-level access is recommended"
- "Uniform bucket-level access cannot be disabled after it has been active on a bucket for 90 consecutive days."

- Page: Discover object storage with the Google Cloud CLI - https://docs.cloud.google.com/storage/docs/discover-object-storage-gcloud
- read at source 2026-11-03 | Last updated 2026-10-30
- `gcloud storage buckets create gs://BUCKET_NAME/ --uniform-bucket-level-access`
- `gcloud storage cp OBJECT_LOCATION gs://BUCKET_NAME`
- `gcloud storage ls gs://BUCKET_NAME`
- `gcloud storage ls gs://BUCKET_NAME/kitten.png --long`
- `gcloud storage rm gs://BUCKET_NAME --recursive`

- Page: Manage external Hive partitioned data (BigQuery) - https://docs.cloud.google.com/bigquery/docs/hive-partitioned-queries
- read at source 2026-11-03 | Last updated 2026-10-27
- Default layout example: "gs://my_bucket/my_table/dt=2019-10-31/lang=en/my_filename"
- Formats: Avro, CSV, JSON, ORC, Parquet.
- Prefix: "a common source URI prefix for all URIs that ends immediately before partition encoding."
- AUTO: "Key names and types are automatically detected."
- STRINGS: "Key names are automatically converted to STRING type."
- CUSTOM: "Partition key schema is encoded as specified in the source URI prefix."
- requirePartitionFilter makes queries without a partition-key predicate fail.

## 8. BigQuery external tables and BigLake tables

- Page: Introduction to external data sources - https://docs.cloud.google.com/bigquery/docs/external-data-sources
- read at source 2026-11-03 | Last updated 2026-10-27
- "External tables let you query structured data in external datastores."
- "BigLake tables let you query structured data in external datastores with access delegation."
- "Access delegation decouples access to the BigLake table from access to the underlying datastore."

- Page: Introduction to BigLake tables - https://docs.cloud.google.com/bigquery/docs/biglake-intro
- read at source 2026-11-03 | Last updated 2026-10-27
- "BigLake tables let you query structured data in Cloud Storage, Amazon S3, and Blob Storage with access delegation."
- "you grant users access only to the BigLake table, not to the underlying datastore."
- Formats: "BigLake tables support the following formats:" Avro, CSV, Delta Lake, Iceberg, JSON, ORC, Parquet.
- Side note: page uses "BigQuery sharing (formerly Analytics Hub)".

## 9. Dataflow and Apache Beam

- Page: Apache Beam Programming Guide - https://beam.apache.org/documentation/programming-guide/
- read at source 2026-11-03 | Last updated: not shown
- "A Pipeline encapsulates your entire data processing task, from start to finish."
- "A PCollection represents a distributed data set that your Beam pipeline operates on."
- "A PTransform represents a data processing operation, or a step, in your pipeline."
- "ParDo is a Beam transform for generic parallel processing."
- "GroupByKey is a Beam transform for processing collections of key/value pairs."
- "Combine is a Beam transform for combining collections of elements or values in your data." (CombinePerKey = per-key form.)
- Fixed: "A fixed time window represents a consistent duration, non overlapping time interval in the data stream."
- Sliding: "sliding time windows can overlap."
- Session: "defines windows that contain elements that are within a certain gap duration of another element."
- Global: "all data in a PCollection is assigned to the single global window, and late data is discarded."

- Page: Using the Direct Runner - https://beam.apache.org/documentation/runners/direct/
- read at source 2026-11-03
- "executes pipelines on your machine"
- "Using the Direct Runner for testing and development helps ensure that pipelines are robust across different Beam runners"
- "not designed for production pipelines"

- Page: Dataflow overview - https://docs.cloud.google.com/dataflow/docs/overview
- read at source 2026-11-03 | Last updated 2026-10-26
- "Dataflow is a Google Cloud service that provides unified stream and batch data processing at scale."
- "Dataflow executes Apache Beam pipelines."
- "To use Dataflow with your Apache Beam pipelines, specify the Dataflow runner." (exact token DataflowRunner NOT FOUND on page)

- Page: Dataflow pricing - https://cloud.google.com/dataflow/pricing
- read at source 2026-11-03 (raw HTML; WebFetch truncated) | Last updated: not shown
- Units: "Worker vCPU and memory (batch, streaming, and FlexRS)", "Dataflow Shuffle data processed (batch and FlexRS)", "Streaming Engine Compute Units or legacy Streaming Engine data processed (streaming only)", "Data Compute Units (DCUs) (batch and streaming)".
- "Dataflow usage is billed in per second increments, on a per job basis."
- Also billed: "Persistent Disk, GPUs, and snapshots."
- Default table rows (default region): "vCPU $0.056 / 1 hour", "Memory $0.003557 / 1 gibibyte hour", "Data Processed during shuffle $0.011 / 1 gibibyte".

## 10. Spark, Pub/Sub, Airflow, scheduled queries

RENAMED: Dataproc is now "Managed Service for Apache Spark"; Cloud Composer is now "Managed Service for Apache Airflow".

- Page: Managed Service for Apache Spark on clusters - https://docs.cloud.google.com/managed-spark/docs/concepts/clusters-overview (old dataproc path redirects here)
- read at source 2026-11-03 | Last updated 2026-10-26
- Banner: "'Managed Service for Apache Spark' is the new name for the product formerly known as 'Dataproc on Compute Engine' (cluster deployment) and 'Google Cloud Serverless for Apache Spark' (serverless deployment)."
- "Managed Service for Apache Spark on clusters lets you take advantage of open source data tools for batch processing, querying, streaming, and machine learning."
- gcloud commands still use `gcloud dataproc` (reported, secondary: search summary of managed-spark docs).
- Rename date: NOT FOUND on page.

- Page: Serverless overview - https://docs.cloud.google.com/managed-spark/docs/serverless-overview (old dataproc-serverless path redirects here)
- read at source 2026-11-03 | Last updated 2026-10-26
- "Managed Service for Apache Spark serverless lets you run Spark workloads without requiring you to provision and manage your own cluster."

- Page: Subscription overview (Pub/Sub) - https://docs.cloud.google.com/pubsub/docs/subscription-overview
- read at source 2026-11-03 | Last updated 2026-10-26
- "Pull subscriptions use a subscriber client to request messages from the Pub/Sub server."
- "Push subscriptions use the Pub/Sub server to initiate requests to your subscriber application to deliver messages."
- "BigQuery subscriptions export data to a BigQuery table."
- "By default, Pub/Sub offers at-least-once delivery with no ordering guarantees on all subscription types."
- "Pub/Sub also supports exactly-once delivery."

- Page: Exactly-once delivery - https://docs.cloud.google.com/pubsub/docs/exactly-once-delivery
- read at source 2026-11-03 | Last updated 2026-10-26
- Only the pull subscription type supports it; "Push and export subscriptions" do not.
- "The exactly-once delivery guarantee only applies when subscribers connect to the service in the same region."

- Page: Managed Airflow overview - https://docs.cloud.google.com/composer/docs/composer-3/composer-overview
- read at source 2026-11-03 | Last updated 2026-10-26
- "Cloud Composer is evolving to become Managed Service for Apache Airflow."
- "Managed Airflow is a fully managed workflow orchestration service."
- Gen 3 supports Airflow 2 and Airflow 3. Rename date: NOT FOUND on page (secondary sources say 2026).

- Page: Scheduling queries - https://docs.cloud.google.com/bigquery/docs/scheduling-queries
- read at source 2026-11-03 | Last updated 2026-10-27
- "Scheduled queries use features of BigQuery Data Transfer Service"
- Minimum interval 5 minutes (as summarised by fetch; verify wording before quoting).

## 11. Cloud Run and Cloud Run functions

- Page: Blog, "Cloud Functions is now Cloud Run functions" - https://cloud.google.com/blog/products/serverless/google-cloud-functions-is-now-cloud-run-functions
- read at source 2026-11-03 | Published August 22, 2024 (James Ma)
- "Cloud Functions and its familiar event-driven programming model is now Cloud Run functions"
- "This goes beyond a simple name change. We've unified the Cloud Functions infrastructure with Cloud Run"
- "we are committed to continuing support for the existing functions APIs, gcloud commands and Terraform modules."

- Page: What is Cloud Run - https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run
- read at source 2026-11-03 | Last updated 2026-10-30
- "On Cloud Run, your code can run as a service, job, worker pool, or instance."
- "Cloud Run services are great for code that handles requests, events, or functions."
- "A job can start a single instance to run your code"
- "Cloud Run functions can respond to asynchronous events, such as a message on a Pub/Sub topic, a change in a Cloud Storage bucket, or a Firebase event."

- Page: Request timeout - https://docs.cloud.google.com/run/docs/configuring/request-timeout
- read at source 2026-11-03 | Last updated 2026-10-30
- "The timeout is set by default to 5 minutes (300 seconds) and can be extended up to 60 minutes (3600 seconds)."

- Page: Task timeout (jobs) - https://docs.cloud.google.com/run/docs/configuring/task-timeout
- read at source 2026-11-03 | Last updated 2026-10-30
- "By default, each task runs for a maximum of 10 minutes."
- Max: "up to 168 hours (7 days)" (GPU tasks: 12 hours, Preview).

- Page: functions-framework-python (GitHub) - https://github.com/GoogleCloudPlatform/functions-framework-python
- read at source 2026-11-03
- `pip install functions-framework`
- `functions-framework --target hello --debug`
- `curl localhost:8080` returns "Hello world!"; PORT / --port default 8080.

- Page: Create a Pub/Sub trigger - https://docs.cloud.google.com/run/docs/triggering/pubsub-triggers
- read at source 2026-11-03 | Last updated 2026-10-31
- "You can invoke Cloud Run services and functions by setting up a Pub/Sub trigger."
- Options: "Direct Pub/Sub trigger (Recommended)" or Eventarc: "Use this if you need Eventarc's advanced filtering or routing features."

- Page: Cloud Run pricing - https://cloud.google.com/run/pricing
- read at source 2026-11-03 (raw HTML; WebFetch truncated) | Last updated: not shown
- Request-based billing: "Free tier (based on us-central1 active pricing): CPU - First 180,000 vCPU-seconds free per month RAM - First 360,000 GiB-seconds free per month Requests - 2 million requests free per month"
- Instance-based billing (services): "CPU - First 240,000 vCPU-seconds free per month RAM - First 450,000 GiB-seconds free per month"
- "The free tier usage is aggregated across projects by billing account and resets every month"

## 12. BigQuery ML

- Page: The CREATE MODEL statement - https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create
- read at source 2026-11-03 | Last updated 2026-10-27
- Variants: CREATE MODEL, CREATE MODEL IF NOT EXISTS, CREATE OR REPLACE MODEL; OPTIONS(model_option_list) with MODEL_TYPE required; optional TRANSFORM; AS query_statement.
- MODEL_TYPE values: LINEAR_REG, BOOSTED_TREE_REGRESSOR, RANDOM_FOREST_REGRESSOR, DNN_REGRESSOR, DNN_LINEAR_COMBINED_REGRESSOR, AUTOML_REGRESSOR, LOGISTIC_REG, BOOSTED_TREE_CLASSIFIER, RANDOM_FOREST_CLASSIFIER, DNN_CLASSIFIER, DNN_LINEAR_COMBINED_CLASSIFIER, AUTOML_CLASSIFIER, KMEANS, MATRIX_FACTORIZATION, PCA, AUTOENCODER, ARIMA_PLUS, ARIMA_PLUS_XREG, CONTRIBUTION_ANALYSIS, TENSORFLOW, TENSORFLOW_LITE, ONNX, XGBOOST (list summarised from the page, not one quote).
- Limit: model must be 90 MB or less (summarised).

- Page: The ML.EVALUATE function - https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate
- read at source 2026-11-03
- "This document describes the ML.EVALUATE function, which lets you evaluate model metrics."

- Page: The ML.PREDICT function - https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict
- read at source 2026-11-03
- "This document describes the ML.PREDICT function, which you can use to predict outcomes by using a model."

- Page: Try BigQuery using the sandbox - https://docs.cloud.google.com/bigquery/docs/sandbox
- read at source 2026-11-03 | Last updated 2026-10-27
- "You are granted a lifetime limit of 10 GiB of storage. This quota is not refunded upon data deletion."
- "the same free compute limit as the BigQuery free tier of 1 TiB of processed query data each month."
- Tables, views and partitions "automatically expire after 60 days."
- Unsupported: "Streaming data", "Data manipulation language (DML) statements", "BigQuery Data Transfer Service".
- No card: "without providing a credit card or creating a billing account for your project."
- BigQuery ML in sandbox: NOT FOUND on page (not listed as unsupported, not mentioned).

- Page: BigQuery pricing (BigQuery ML section) - https://cloud.google.com/bigquery/pricing
- read at source 2026-11-03 (raw HTML) | Last updated: not shown
- "BigQuery ML jobs that perform inspection, evaluation, and prediction operations incur the same charges as on-demand query jobs."
- "Because CREATE MODEL queries incur different charges, you must calculate CREATE MODEL job costs independently"
- On-demand built-in model creation (linear, logistic, k-means, PCA, time series, contribution analysis) row shows "$312.50 / 1 tebibyte"; external models (AutoML, DNN, boosted tree, random forest, autoencoder) show "$6.25 / 1 tebibyte" plus passthrough training cost. Table flattened in raw HTML; confirm row mapping visually before quoting.
- "BigQuery ML is available in Enterprise and Enterprise Plus Editions"
- "The CREATE MODEL statement stops at 50 iterations for iterative models."
- "Matrix factorization models are only available to editions customers or customers with reservations."

## 13. Vertex AI (now Gemini Enterprise Agent Platform)

RENAMED: Vertex AI is now "Gemini Enterprise Agent Platform" (short: Agent Platform), from April 22, 2026. Old vertex-ai docs URLs redirect to /gemini-enterprise-agent-platform/.

- Page: Agent Platform release notes - https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes
- read at source 2026-11-03
- "April 22, 2026 Change Vertex AI to Gemini Enterprise Agent Platform naming changes"
- Table pairs (verbatim names): Vertex AI Model Garden -> "Model Garden"; Vertex AI Pipelines -> "Agent Platform Pipelines"; Vertex AI Model Registry -> "Agent Platform Model Registry"; Vertex AI Endpoints -> "Agent Platform Endpoints"; Vertex AI Workbench -> "Agent Platform Workbench"; Vertex AI Training -> "Agent Platform Managed Training"; Vertex AI Studio -> "Agent Studio"; Vertex AI Agent Engine -> "Agent Runtime".

- Page: Agent Platform ML overview - https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning (old /vertex-ai/docs/start/introduction-unified-platform)
- read at source 2026-11-03 | Last updated 2026-10-30
- "Gemini Enterprise Agent Platform provides a comprehensive suite of tools"
- Training: "a managed training service that helps you operationalize large-scale model training"
- "The Model Registry is a central repository where you can manage the lifecycle of" ML models.
- The words "unified ML platform" and "Vertex AI": NOT FOUND on page.

- Page: Agent Platform home - https://docs.cloud.google.com/gemini-enterprise-agent-platform
- "Gemini Enterprise Agent Platform is our open and comprehensive platform that empowers businesses to rapidly build, scale, govern, and optimize enterprise-grade agents"

- Page: Pipelines intro - https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/pipelines/introduction
- "Agent Platform Pipelines lets you automate, monitor, and govern your machine learning (ML) systems in a serverless manner"

- Page: Overview of Model Garden - https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-garden/explore-models
- "Model Garden is an AI/ML model library that helps you discover, test, customize, and deploy models and assets from Google and Google partners."

- Page: Workbench introduction - https://docs.cloud.google.com/gemini-enterprise-agent-platform/notebooks/workbench/introduction
- read at source 2026-11-03 | Last updated 2026-11-02
- "Gemini Enterprise Agent Platform Workbench instances are Jupyter notebook-based development environments"

- Page: Claude on Google Cloud - https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude
- read at source 2026-11-03 | Last updated 2026-11-02
- "The Anthropic Claude models on Google Cloud offer fully managed and serverless models as APIs."
- "To access a Claude on Google Cloud model, go to its Model Garden model card."

## 14. Knowledge Catalog (formerly Dataplex), column and row security

RENAMED: Dataplex Universal Catalog is now "Knowledge Catalog" as of April 10, 2026.

- Page: Knowledge Catalog introduction - https://docs.cloud.google.com/knowledge-catalog/docs/introduction (old /dataplex/docs/introduction redirects here)
- read at source 2026-11-03 | Last updated 2026-10-29
- "As of April 10, 2026, Dataplex Universal Catalog is now called Knowledge Catalog. The API, client library, CLI, and IAM names remain unchanged."
- "Knowledge Catalog lets you unify technical metadata and business semantics across structured and unstructured data."
- Profiling scans check for "schema anomalies and statistical drift."
- Docs nav lists "About data profiling" and "Data quality tasks (legacy)".
- Lakes / zones / assets: NOT FOUND on the current intro; /dataplex/docs/terminology now redirects to the Knowledge Catalog overview and /dataplex/docs/introduction-to-lakes returns 404. Older definitions reported (secondary: search summary of https://docs.cloud.google.com/dataplex/docs/terminology?hl=en and gcloud reference https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/zones/create): lake = logical construct for a data domain; zone = subdomain in a lake (raw / curated); asset = maps to data in Cloud Storage or BigQuery. Treat lakes/zones as legacy.

- Page: Introduction to column-level access control - https://docs.cloud.google.com/bigquery/docs/column-level-security-intro
- read at source 2026-11-03 | Last updated 2026-10-27
- Columns restricted with "policy tags (based on Data Catalog)" or data governance tags.
- "Taxonomies are regional resources, like BigQuery datasets and tables."
- Role ID shown as datacatalog.categoryFineGrainedReader (Fine-Grained Reader); "roles/" prefix not shown on page.
- "Column-level access control is enforced in addition to existing dataset ACLs."
- Limits: hierarchy max five levels deep; max 1,000 unique policy tags per table (summarised).

- Page: Introduction to BigQuery row-level security - https://docs.cloud.google.com/bigquery/docs/row-level-security-intro
- read at source 2026-11-03 | Last updated 2026-10-27
- A policy identifies "which users or groups (called the grantee-list) can access certain row data."
- The filter_expression "functions like a WHERE clause in a typical query."

## 15. Google Cloud Well-Architected Framework

- Page: Google Cloud Well-Architected Framework - https://docs.cloud.google.com/architecture/framework
- read at source 2026-11-03 | Last updated 2026-10-13
- Current name on page: "Well-Architected Framework" ("Architecture Framework" survives only in the URL path). "formerly" note: NOT FOUND on page.
- Pillars: "Operational excellence", "Security, privacy, and compliance", "Reliability", "Cost optimization", "Performance optimization", "Sustainability".

## 16. Professional Data Engineer exam

- Page: Professional Data Engineer certification - https://cloud.google.com/learn/certification/data-engineer
- read at source 2026-11-03
- "Length: 2 hours" | "Registration fee: $200 (plus tax where applicable)" | "Languages: English, Japanese"
- "Exam format: 40 - 50 multiple choice and multiple select questions"
- "Validity period: 2 years" | "Prerequisites: None"
- "Recommended experience: 3+ years of industry experience including 1+ years designing and managing data solutions using Google Cloud."
- Renewal exam: "Length: 1 hour", "$100", "20 multiple choice and multiple select questions".

- Page: Exam guide PDF - https://services.google.com/fh/files/misc/professional_data_engineer_exam_guide_english.pdf
- read at source 2026-11-03 (5 pages, no date)
- "Section 1: Designing data processing systems (~22% of the exam)" - 1.1 Designing for security and compliance; 1.2 Designing for reliability and fidelity; 1.3 Designing for flexibility and portability; 1.4 Designing data migrations.
- "Section 2: Ingesting and processing the data (~25% of the exam)" - 2.1 Planning the data pipelines; 2.2 Building the pipelines; 2.3 Deploying and operationalizing the pipelines.
- "Section 3: Storing the data (~20% of the exam)" - 3.1 Selecting storage systems; 3.2 Planning for using a data warehouse; 3.3 Using a data lake; 3.4 Designing for a data platform.
- "Section 4: Preparing and using data for analysis (~15% of the exam)" - 4.1 Preparing data for visualization; 4.2 Preparing data for AI and ML; 4.3 Sharing data.
- "Section 5: Maintaining and automating data workloads (~18% of the exam)" - 5.1 Optimizing resources; 5.2 Designing automation and repeatability; 5.3 Organizing workloads based on business requirements; 5.4 Monitoring and troubleshooting processes; 5.5 Maintaining awareness of failures and mitigating impact.
- Guide still says "Creating directed acyclic graphs (DAGs) for Cloud Composer" and "BigQuery sharing (Analytics Hub)" (pre-rename names).

- Learning path: "Professional Data Engineer Certification" (13 activities) - https://www.skills.google/paths/16 (cloudskillsboost.google/paths/16 now 308-redirects to skills.google)

## 17. BigQuery editions and slots

- Page: Understand BigQuery editions - https://docs.cloud.google.com/bigquery/docs/editions-intro
- read at source 2026-11-03 | Last updated 2026-10-27
- "BigQuery provides three editions which support different types of workloads." (Standard, Enterprise, Enterprise Plus)
- Commitments (Enterprise, Enterprise Plus): "1-year commitment at 20% discount or 3-year commitment at 40% discount."
- Standard: "No access to BigQuery ML."; max reservation size 1,600 slots.
- "Capacity commitments are not required to purchase slots, but can reduce costs."

- Page: Understand slots - https://docs.cloud.google.com/bigquery/docs/slots (old slots-autoscaling-intro redirects to #slot-autoscaling)
- read at source 2026-11-03 | Last updated 2026-10-27
- "Slots always autoscale to a multiple of 50."
- "The baseline is the minimum number of slots that will always be allocated to the reservation."
- Cap via "a maximum number of slots (the max reservation size)".

- Page: BigQuery pricing - https://cloud.google.com/bigquery/pricing
- read at source 2026-11-03 (raw HTML)
- "Capacity pricing (per slot-hour)" ... "measured in slots (virtual CPUs) over time."
- "is billed per second with a one-minute minimum duration by default." Fluid scaling opt-in gives no-minimum per-second billing.
- Commitments "are available in Enterprise and Enterprise Plus editions" and "are offered with a 50-slot minimum and increments of 50 slots."
- Pay-as-you-go per slot-hour in the default table of the static page (region list starts at Iowa us-central1; US multi-region selection NOT verifiable without the JS region picker): Standard "$0.04 / 1 hour"; Enterprise "$0.06 / 1 hour"; Enterprise Plus "$0.10 / 1 hour".
- On-demand: "1 tebibyte and above $6.25 / 1 tebibyte"; "up to 2,000 concurrent slots, shared among all queries in a single project."
- Inter-region transfer: "Cross-region load jobs are billed for network usage under Network Data Transfer SKUs."
- Also: "Cross-region extract jobs are billed under General Data Transfer Networking Traffic for Google Cloud Cross Region SKUs."

## 18. BigQuery cost controls and budgets

- Page: Create custom query quotas - https://docs.cloud.google.com/bigquery/docs/custom-quotas
- read at source 2026-11-03 | Last updated 2026-10-27
- "Project-level custom quotas limit the aggregate usage of all users in that project." (QueryUsagePerDay)
- User level: QueryUsagePerUserPerDay.
- If the project quota is hit, "BigQuery stops working for everyone in that project" until reset.
- Default QueryUsagePerDay: "200 Tebibytes (TiB) of data processed per project per day"; per-user default unlimited.

- Page: Estimate and control costs - https://docs.cloud.google.com/bigquery/docs/best-practices-costs
- read at source 2026-11-03 | Last updated 2026-10-27
- Maximum bytes billed: "then the query fails without incurring a charge."
- "applying a LIMIT clause to a query doesn't affect the amount of data that is read."
- "Before running queries, preview them to estimate costs."

- Page: Create, edit, or delete budgets and budget alerts - https://docs.cloud.google.com/billing/docs/how-to/budgets
- read at source 2026-11-03 | Last updated 2026-10-26
- "Setting an alerts-only budget doesn't automatically cap Google Cloud or Google Maps Platform usage or spending."
- "For alerts-only budgets, the budget doesn't automatically set a hard cap on spending."
- NEW: "If supported for your service, you can configure spend cap budgets on a project."

- Page: Manage spend cap budgets - https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps
- read at source 2026-11-03 | Last updated 2026-10-26
- "Spend caps are a cost control mechanism. A spend cap is enforced when usage costs exceed your budget target amount."
- Eligible: "Gemini API, Agent Platform (formerly known as Vertex AI), Cloud Run, and Cloud Run functions." BigQuery is NOT eligible.
- "Spend caps are limited to budgets that are scoped to a single Google Cloud project and a single eligible service"
- "Any overage due to cost reporting latency is billed as usual."
- Launch stage: Preview (reported, secondary: billing release notes feed / https://medium.com/@avnitbambah/gcp-finally-has-a-kill-switch-spend-cap-budgets-arrive-in-preview-002a8ceca318); NOT FOUND on page.

## 19. Cloud Billing, Free Trial, Free Tier

- Page: Cloud Billing concepts - https://docs.cloud.google.com/billing/docs/concepts
- read at source 2026-11-03 | Last updated 2026-10-26
- A Cloud Billing account "defines who pays for a given set of Google Cloud resources and Google Maps Platform APIs."
- Payment linkage defines "which Cloud Billing account pays for a given project."
- Example billing account "is linked to Projects 1, 2, and 3".
- "A project links to at most one billing account": NOT FOUND as a sentence on page.

- Page: Free cloud features and trial offer - https://docs.cloud.google.com/free/docs/free-cloud-features
- read at source 2026-11-03 | Last updated 2026-10-27
- "The Free Trial gets you a $300 Welcome credit to spend over 90 days on various Google Cloud products and you won't be billed."
- Card required: "you must provide a credit card or other payment method that is valid for the period of the Free Trial."
- "You'll only be billed for usage that exceeds your remaining credit." (after upgrade)
- BigQuery Free Tier: "1 TiB of querying per month" and "10 GiB of storage per month."
- Cloud Storage: "5 GB-months of regional storage (US regions only) per month."
- Cloud Run: "2 million requests per month" and "360,000 GB-seconds of memory, 180,000 vCPU-seconds of compute time."
- Cloud Run functions: "2 million invocations per month (includes both background and HTTP invocations)."

---

## Not found / uncertain

1. IAM "no way to remove an inherited permission with an allow policy": no Google sentence found; only third-party. Teach it from "union" + deny policies.
2. Deny-policy example `bigquery.googleapis.com/tables.getData`: not on the deny page (format SERVICE_FQDN/RESOURCE.ACTION is; example given is iam.googleapis.com/roles.delete).
3. BigQuery ML in the sandbox: not mentioned on the sandbox page or pricing page.
4. BigQuery pay-as-you-go slot prices for the US multi-region specifically: static HTML only shows the default table (list starts at Iowa); $0.04 / $0.06 / $0.10 not confirmed for US multi-region.
5. BQML on-demand CREATE MODEL rate mapping ($312.50/TiB built-in vs $6.25/TiB external + passthrough) read from a flattened table; confirm visually.
6. Dataplex lakes / zones / assets: removed from current docs (404 / redirect); definitions only from secondary summaries.
7. Rename dates for Managed Service for Apache Spark and Managed Service for Apache Airflow: not on pages.
8. Spend cap launch stage (Preview): not on the page; secondary only.
9. Max lifecycle rules per bucket; general BigQuery dataset-location immutability: not on pages read.
10. "Last updated" for cloud.google.com pricing pages and beam.apache.org: not shown.
11. Scheduled queries 5-minute minimum: from fetch summary, not a verified verbatim quote.
