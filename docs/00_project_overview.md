# AI Test Analytics Hub – Project Overview

## 1. Purpose

The AI Test Analytics Hub (TARH) is a cloud-native platform designed to analyze 
test case outcomes, defect trends, and release data using predictive machine 
learning models and generative AI. 

The project serves two primary goals:

1. **Build hands-on expertise in AWS cloud architecture**  
   (serverless, storage, databases, networking, identity, automation)

2. **Develop practical AI/ML solutions**  
   (EDA → feature engineering → classical ML → GenAI with AWS Bedrock)

---

## 2. What the Platform Will Do

- Ingest test cases, defects, and release datasets
- Compute baseline analytics (failure rate, defect density, high-risk areas)
- Train ML models to:
  - Predict failure probability of test cases
  - Identify defect-prone modules
  - Forecast defect volume for upcoming releases
- Provide a modern UI dashboard for:
  - Trends, charts, analysis, insights
- Provide an AI assistant for:
  - Natural language question answering
  - Test case generation from requirements
  - Summarization of defect clusters

---

## 3. Target AWS Architecture (Phases 1–3)

- **UI Layer:**  
  React + Tailwind, hosted on **S3 + CloudFront** or **AWS Amplify Hosting**

- **Identity:**  
  Amazon **Cognito** (User Pools + JWT integration)

- **APIs:**  
  Amazon **API Gateway** + AWS **Lambda** (serverless backend)

- **Data Stores:**  
  - Amazon **Aurora Serverless v2** (structured relational data)
  - Amazon **DynamoDB** (feature cache + chat context)
  - Amazon **S3** (raw data, processed data, ML artifacts)

- **AI/ML:**  
  - **SageMaker** (classical ML training + endpoints)  
  - **AWS Bedrock** (GenAI for conversational capabilities)

- **Orchestration:**  
  - AWS **EventBridge** (scheduled jobs)
  - AWS **Step Functions** (ML pipelines in Phase 3)

---

## 4. Phase Roadmap

### **Phase 0 — Local ML Foundation (Current Phase)**
- Create GitHub repo
- Store initial sample datasets
- Establish ML workspace
- Perform basic EDA and baseline analysis

### **Phase 1 — AWS Foundations**
- Create AWS accounts, IAM roles, VPC setup
- Configure Aurora, S3, API Gateway, Lambda skeleton
- Implement ingestion pipeline

### **Phase 2 — Classical ML with SageMaker**
- Feature engineering
- Model training + tuning (XGBoost, Random Forest)
- Deploy SageMaker endpoint
- Integrate ML inference with Lambda/API

### **Phase 3 — GenAI + RAG using Bedrock**
- Embedding + vector store (OpenSearch Serverless)
- QA over test cases, defects, and release notes
- Build a conversational QA assistant in UI

### **Phase 4 — CI/CD + DevOps**
- GitHub Actions OR AWS CodePipeline
- IaC with AWS CDK or Terraform
- Automated test + deploy workflows

---

## 5. Key Benefits

- Learn full-stack AWS architecture  
- Build ML + GenAI skills for your portfolio  
- Produce a project demonstrable during interviews  
- Future expandability into enterprise test analytics
