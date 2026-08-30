# Google Cloud Project Selection

## Current Account
barathwaj61@gmail.com

## Current Project
semiotic-dock-7nm9t

## Why Current Project Is Restricted
The account only has limited viewer and free-tier user roles (`roles/firebase.viewer`, `roles/run.viewer`, `roles/datastore.user`, etc.). It lacks the administrative privileges (`roles/owner` or `roles/editor`) necessary to enable APIs, create Cloud Run services, or fully configure Firestore. IAM modifications failed because the account does not have `resourcemanager.projects.setIamPolicy` permission on this project. It should be abandoned for this deployment.

## Accessible Projects

| Project ID | Role | Admin Access | Billing Status | Suitable |
|---|---|---|---|---|
| project-03e8aedb-c10e-4ed4-a0a | roles/owner | Yes | Disabled | Partial |
| project-c37e8218-69e6-4be4-bbe | roles/owner | Yes | Disabled | Partial |
| project-c961c60a-5f6d-431b-8f1 | roles/owner | Yes | Disabled | Partial |
| project-edb2161c-69e7-4516-a9c | roles/owner | Yes | Disabled | Partial |
| project-3c2858a0-975f-48ce-afe | roles/owner | Yes | Disabled | Partial |
| project-8e22a0b0-563f-437c-814 | roles/owner | Yes | Disabled | Partial |
| project-a0c076ae-5bbd-4a9e-989 | roles/owner | Yes | Disabled | Partial |
| semiotic-dock-7nm9t | Viewer/FreeTier | No | Enabled | No |
| abstract-proxy-rlcf1 | (No Access) | No | Enabled | No |
| project-32da1bf8-802d-43e6-959 | roles/owner | Yes | Disabled | Partial |
| project-269ae956-aecf-440e-a24 | roles/owner | Yes | Disabled | Partial |
| project-1f5496af-1664-4fa8-9ff | roles/owner | Yes | Disabled | Partial |
| project-f80c7661-d5f9-4e78-b57 | roles/owner | Yes | Disabled | Partial |
| gen-lang-client-0284521778 | roles/owner | Yes | Disabled | Partial |

## Recommended Project

Project ID: gen-lang-client-0284521778
Project Name: Default Gemini Project
Reason: This project is explicitly owned by the account (`roles/owner`) and is already associated with Gemini APIs (`generativelanguage.googleapis.com` is enabled). It has the necessary admin access to deploy VERDICT natively, provided billing is activated.

## Projects Rejected
- `semiotic-dock-7nm9t` - Insufficient IAM permissions (Viewer only).
- `abstract-proxy-rlcf1` - No access.
- `project-*` (others) - All lack billing and lack pre-existing Gemini API alignment.

## Next Manual Action
The recommended project (`gen-lang-client-0284521778`) currently does not have billing enabled. Cloud Run requires an active billing account.
1. Enable billing for `gen-lang-client-0284521778` in the Google Cloud Console.
2. Run: `gcloud config set project gen-lang-client-0284521778`
3. Run: `gcloud auth application-default login`
