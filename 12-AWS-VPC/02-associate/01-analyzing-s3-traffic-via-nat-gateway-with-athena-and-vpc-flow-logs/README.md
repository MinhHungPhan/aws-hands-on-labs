# Analyzing S3 traffic via NAT Gateway with Athena and VPC Flow Logs

Have you ever wondered why your AWS bill includes unexpected charges from NAT Gateway data processing? Well, you're not alone. One of the biggest money-wasters in AWS happens when your applications send data to S3 storage through NAT Gateways (the expensive route) instead of using S3 Gateway endpoints (the free, direct route that AWS provides).

## Table of Contents

- [Introduction](#introduction)
- [What You'll Learn](#what-youll-learn)
- [Prerequisites](#prerequisites)
- [Understanding the Problem](#understanding-the-problem)
- [Lab Setup and Configuration](#lab-setup-and-configuration)
- [Creating the Athena Table](#creating-the-athena-table)
- [Analyzing S3 Traffic Patterns](#analyzing-s3-traffic-patterns)
- [Advanced Analysis Techniques](#advanced-analysis-techniques)
- [Best Practices](#best-practices)
- [Key Takeaways](#key-takeaways)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

This hands-on lab will guide you through a practical approach to detect and analyze such traffic patterns using Amazon Athena and VPC Flow Logs. By the end of this tutorial, you'll have the skills to identify which VPCs or resources are missing S3 Gateway endpoints, potentially saving your organization significant costs while improving network performance.

The beauty of this approach lies in its simplicity - we're essentially using AWS's own logging capabilities to uncover inefficient traffic patterns that might otherwise go unnoticed.

## What You'll Learn

By completing this lab, you'll gain hands-on experience with:
- Setting up VPC Flow Logs for Transit Gateway attachments
- Creating external tables in Amazon Athena for log analysis
- Writing SQL queries to identify cost-optimization opportunities
- Understanding AWS network traffic patterns and routing behavior
- Implementing account mapping for better data visualization

## Prerequisites

Before diving into this lab, you should have:

- **AWS Account Access**: Administrative or sufficient permissions to access Athena, VPC, and Transit Gateway services
- **Basic SQL Knowledge**: Comfort with writing SELECT statements and basic joins
- **AWS CLI Installed**: For generating account mapping data (optional but recommended)
- **Understanding of AWS Networking**: Basic familiarity with VPCs, subnets, and NAT Gateways

**Note**: This lab assumes you're working in an environment with centralized NAT Gateways and Transit Gateway connectivity - a common enterprise AWS setup.

## Understanding the Problem

Let me paint a picture of what we're trying to solve here. In many enterprise AWS environments, you'll find a centralized network architecture where:

1. **Outbound internet traffic** flows through centralized NAT Gateways
2. **Cross-VPC connectivity** is managed via Transit Gateways
3. **S3 access** might inadvertently route through these expensive components

The issue arises when VPCs lack S3 Gateway endpoints. Without these endpoints, S3 traffic takes a costly detour:
- Traffic originates from your application in a private subnet
- Instead of going directly to S3, it routes to the NAT Gateway
- The NAT Gateway processes and forwards the traffic (costing money)
- If using Transit Gateway, additional charges apply

This routing pattern can result in unnecessary charges that, frankly, many organizations don't realize they're paying for.

## Lab Setup and Configuration

### Step 1: Enable VPC Flow Logs

First, we need to enable Flow Logs on the Transit Gateway attachment. This is where the magic happens—these logs will capture all the network traffic patterns we need to analyze.

1. Navigate to the **VPC Console** in your AWS account
2. Go to **Transit Gateways** → **Transit Gateway Attachments**
3. Find your outbound VPC attachment (typically named something like `INTERNET-ZONE-outbound-traffic`)
4. Enable Flow Logs with the following configuration:
   - **Destination**: S3 bucket
   - **Log Format**: Custom (we'll need specific fields)
   - **Capture**: All traffic (accepted and rejected)

### Step 2: Set Up Amazon Athena

Navigate to the Amazon Athena console. This step is crucial for first-time Athena users, as you'll need to configure where Athena stores query results.

#### Configure Query Result Location

When you first open the Athena console, you'll likely see a banner message saying "Before you run your first query, you need to set up a query result location in Amazon S3." Here's how to set this up:

1. **Click "Settings" or "Manage settings"** in the Athena console
2. **Specify an S3 location** for query results. You can either:
   - Use an existing S3 bucket: `s3://your-existing-bucket/athena-results/`
   - Create a new bucket specifically for Athena results

**Example Configuration:**

```
Query result location: s3://my-company-athena-results/vpc-flow-analysis/
Encryption: AES-256 (recommended for sensitive network data)
```

3. **Save the settings** - this is a one-time setup per region

#### Why This Matters

Amazon Athena is serverless and doesn't store data itself. When you run SQL queries, Athena needs somewhere to save the results (typically as CSV files). Think of it as Athena's "scratch space" for your query outputs.

**Cost Tip**: Consider setting up S3 lifecycle policies to automatically delete query results older than 30-90 days to manage storage costs.

**Important**: Make sure you're in the correct AWS region where your VPC Flow Logs are stored before proceeding.

### Step 3: Understanding Your Flow Log Structure

Before creating the Athena table, you need to understand how your VPC Flow Logs are organized in S3. This step is crucial for building an accurate table definition.

#### Examine Your S3 Bucket Structure

First, let's explore where your flow logs are stored:

```bash
# List the top-level structure
aws s3 ls s3://your-flow-logs-bucket/

# Drill down to see the date-based organization
aws s3 ls s3://your-flow-logs-bucket/AWSLogs/123456789012/vpcflowlogs/us-east-1/ --recursive | head -20
```

**Typical S3 path structure:**

```
s3://my-flow-logs-bucket/
  └── AWSLogs/
      └── 123456789012/              # Your AWS Account ID
          └── vpcflowlogs/
              └── us-east-1/          # AWS Region
                  └── 2025/           # Year
                      └── 11/         # Month
                          └── 07/     # Day
                              └── 123456789012_vpcflowlogs_us-east-1_fl-1234abcd_20251107T0000Z_hash.log.gz
```

#### Download and Examine a Sample Log File

To build the correct table schema, you need to see what fields are actually in your logs:

```bash
# Download a sample log file
aws s3 cp s3://your-flow-logs-bucket/AWSLogs/123456789012/vpcflowlogs/us-east-1/2025/11/07/sample.log.gz .

# Decompress and view the first few lines
gunzip sample.log.gz
head -5 sample.log
```

**Example log file header (Transit Gateway format):**

```
version resource-type account-id tgw-id tgw-attachment-id tgw-src-vpc-account-id tgw-dst-vpc-account-id tgw-src-vpc-id tgw-dst-vpc-id tgw-src-subnet-id tgw-dst-subnet-id tgw-src-eni tgw-dst-eni tgw-src-az-id tgw-dst-az-id tgw-pair-attachment-id srcaddr dstaddr srcport dstport protocol packets bytes start end log-status type packets-lost-no-route packets-lost-blackhole packets-lost-mtu-exceeded packets-lost-ttl-expired tcp-flags region flow-direction pkt-src-aws-service pkt-dst-aws-service
```

**Example data line:**

```
5 TransitGatewayAttachment 123456789012 tgw-0abc123 tgw-attach-0xyz789 123456789012 123456789012 vpc-0abc123 vpc-0def456 subnet-0abc123 subnet-0def456 eni-0abc123 eni-0def456 use1-az1 use1-az2 - 10.0.1.50 52.218.196.0 54321 443 6 150 12500 1699315200 1699315260 OK IPv4 0 0 0 0 2 us-east-1 egress - S3
```

#### Map Fields to SQL Data Types

Understanding the data types is essential for accurate querying:

| Field Name | Sample Value | SQL Type | Reasoning |
|------------|--------------|----------|-----------|
| `version` | `5` | `int` | Flow log format version |
| `resource_type` | `TransitGatewayAttachment` | `string` | Text identifier |
| `account_id` | `123456789012` | `string` | Keep as string (may have leading zeros) |
| `srcaddr` | `10.0.1.50` | `string` | IP addresses are text |
| `srcport` | `54321` | `int` | Port numbers are integers |
| `bytes` | `12500` | `bigint` | Can be very large values |
| `start` | `1699315200` | `bigint` | Unix timestamps |
| `end` | `1699315260` | `bigint` | Reserved keyword - needs backticks |
| `pkt_dst_aws_service` | `S3` | `string` | Service name (S3, DYNAMODB, etc.) |

**Important Notes:**
- Use `string` for IDs and IP addresses (even if they look numeric)
- Use `bigint` for byte counts and timestamps (they can exceed `int` range)
- Use backticks for reserved SQL keywords like `end`
- Fields with hyphens in the log are converted to underscores in SQL (e.g., `resource-type` → `resource_type`)

#### Alternative: Use AWS Glue Crawler (Automated Approach)

If you prefer AWS to automatically detect your schema, you can use a Glue Crawler:

```bash
# Create a Glue Crawler
aws glue create-crawler \
  --name vpc-flow-logs-crawler \
  --role AWSGlueServiceRole-FlowLogs \
  --database-name vpc_logs_db \
  --targets "S3Targets=[{Path=s3://your-flow-logs-bucket/AWSLogs/}]"

# Run the crawler
aws glue start-crawler --name vpc-flow-logs-crawler

# Check status
aws glue get-crawler --name vpc-flow-logs-crawler
```

The Glue Crawler will:
- ✅ Automatically detect field names and data types
- ✅ Create the table in Athena
- ✅ Identify existing partitions
- ⚠️ May require manual optimization for partition projection

**When to use Glue Crawler:**
- First time working with VPC Flow Logs
- Unsure about the exact schema
- Want quick setup without manual configuration

**When to manually create the table:**
- Need partition projection for better performance
- Want full control over data types
- Working with custom log formats

## Creating the Athena Table

Now comes the technical part—creating an external table that points to our VPC Flow Logs. This table structure is specifically designed to capture Transit Gateway flow log data.

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS vpc_flow_logs_tgw_attachment_outbound (
    version int,
    resource_type string,
    account_id string,
    tgw_id string,
    tgw_attachment_id string,
    tgw_src_vpc_account_id string,
    tgw_dst_vpc_account_id string,
    tgw_src_vpc_id string,
    tgw_dst_vpc_id string,
    tgw_src_subnet_id string,
    tgw_dst_subnet_id string,
    tgw_src_eni string,
    tgw_dst_eni string,
    tgw_src_az_id string,
    tgw_dst_az_id string,
    tgw_pair_attachment_id string,
    srcaddr string,
    dstaddr string,
    srcport int,
    dstport int,
    protocol bigint,
    packets bigint,
    bytes bigint,
    start bigint,
    `end` bigint,
    log_status string,
    type string,
    packets_lost_no_route bigint,
    packets_lost_blackhole bigint,
    packets_lost_mtu_exceeded bigint,
    packets_lost_ttl_expired bigint,
    tcp_flags int,
    region string,
    flow_direction string,
    pkt_src_aws_service string,
    pkt_dst_aws_service string
)
PARTITIONED BY (day string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '
LOCATION 's3://your-flow-logs-bucket/path-to-logs/'
TBLPROPERTIES (
    "skip.header.line.count" = "1",
    "projection.enabled" = "true",
    "projection.day.type" = "date",
    "projection.day.range" = "2025/01/01,NOW",
    "projection.day.format" = "yyyy/MM/dd",
    "storage.location.template" = "s3://your-flow-logs-bucket/path-to-logs/${day}"
);
```

**Important**: Replace `your-flow-logs-bucket` and `path-to-logs` with your actual S3 bucket and path information.

The partition projection feature is quite clever here—it automatically handles date-based partitioning without requiring manual partition management. This means Athena can efficiently query data across different days without scanning unnecessary files.

### Validating Your Table Setup

After creating the table, it's essential to validate that everything is working correctly. Here's how to test your setup:

#### Test 1: Basic Table Query

Start with a simple query to verify Athena can read your data:

```sql
-- Retrieve the first 10 records
SELECT * 
FROM vpc_flow_logs_tgw_attachment_outbound 
LIMIT 10;
```

**What to look for:**
- ✅ Query completes successfully
- ✅ Data appears with proper column values
- ❌ If you get "HIVE_CANNOT_OPEN_SPLIT" error, check your S3 path
- ❌ If columns are NULL, verify your field delimiter matches the log format

#### Test 2: Verify Partition Projection

Check if partition projection is working correctly:

```sql
-- Count records for a specific date
SELECT COUNT(*) as record_count
FROM vpc_flow_logs_tgw_attachment_outbound 
WHERE day = '2025/11/07';
```

**Expected behavior:**
- Query should complete in seconds (not minutes)
- If it's slow, partition projection may not be working
- Check that your `storage.location.template` matches your actual S3 structure

#### Test 3: Validate S3 Traffic Detection

Verify that you can identify S3 traffic:

```sql
-- Check what AWS services are in your logs
SELECT pkt_dst_aws_service, 
       COUNT(*) as request_count,
       ROUND(SUM(bytes / 1073741824.0), 2) as total_gb
FROM vpc_flow_logs_tgw_attachment_outbound
WHERE pkt_dst_aws_service IS NOT NULL
GROUP BY pkt_dst_aws_service
ORDER BY total_gb DESC;
```

**What you should see:**
- S3 should appear in the results (if you have S3 traffic)
- Other services like DYNAMODB, EC2, etc., may also appear
- Byte counts should be reasonable (not zeros or extremely large values)

### Troubleshooting Table Creation Issues

#### Problem: "HIVE_CANNOT_OPEN_SPLIT" Error

**Cause:** S3 path in the `LOCATION` or `storage.location.template` doesn't match your actual structure.

**Solution:**

```sql
-- Verify your S3 path structure
-- Run this in your terminal:
aws s3 ls s3://your-flow-logs-bucket/ --recursive | grep 2025/11/07 | head -5

-- Compare with your storage.location.template
-- It should match: s3://bucket/path/${day}
-- where ${day} is replaced with 2025/11/07
```

#### Problem: All Fields Return NULL

**Cause:** Field delimiter mismatch or incorrect schema.

**Solution:**

```sql
-- Drop and recreate the table with correct delimiter
DROP TABLE vpc_flow_logs_tgw_attachment_outbound;

-- VPC Flow Logs use space delimiter
-- Make sure you have: FIELDS TERMINATED BY ' '
-- NOT: FIELDS TERMINATED BY ','
```

#### Problem: Query Returns No Data

**Cause:** Date range in partition projection doesn't include your data.

**Solution:**

```sql
-- Check what dates actually exist in your S3 bucket
-- In terminal:
aws s3 ls s3://your-flow-logs-bucket/path-to-logs/ --recursive | grep "\.log" | head -20

-- Update your table properties with correct date range
ALTER TABLE vpc_flow_logs_tgw_attachment_outbound 
SET TBLPROPERTIES (
    "projection.day.range" = "2025/01/01,NOW"
);
```

#### Problem: "Access Denied" Error

**Cause:** Athena doesn't have permission to read your S3 bucket.

**Solution:**

```json
// Add this policy to your Athena execution role:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-flow-logs-bucket",
                "arn:aws:s3:::your-flow-logs-bucket/*"
            ]
        }
    ]
}
```

### Understanding Your Table Properties

Let's break down what each table property does:

```sql
TBLPROPERTIES (
    -- Skip the header line in each log file
    "skip.header.line.count" = "1",
    
    -- Enable automatic partition discovery
    "projection.enabled" = "true",
    
    -- Define partition as date type
    "projection.day.type" = "date",
    
    -- Date range: from start date to NOW (current date)
    "projection.day.range" = "2025/01/01,NOW",
    
    -- Date format matching your S3 structure
    "projection.day.format" = "yyyy/MM/dd",
    
    -- Template for S3 path with partition variable
    "storage.location.template" = "s3://your-bucket/path/${day}"
);
```

**Why partition projection matters:**
- ❌ Without it: Athena scans ALL files in your bucket (slow + expensive)
- ✅ With it: Athena only scans files in the specified date range (fast + cheap)

**Example cost difference:**
- Scanning 1 TB of data: ~$5.00
- Scanning 10 GB with partition projection: ~$0.05

That's a 100x cost reduction for date-filtered queries!

## Analyzing S3 Traffic Patterns

### Query 1: Total S3 Traffic Volume Through NAT

Let's start with the big picture—how much S3 traffic is unnecessarily flowing through your NAT Gateway?

```sql
SELECT sum(bytes / 1073741824.0) AS total_gbytes
FROM "default"."vpc_flow_logs_tgw_attachment_outbound"
WHERE pkt_dst_aws_service = 'S3'
ORDER BY total_gbytes;
```

This query converts bytes to gigabytes (hence the division by 1073741824) and shows the total volume. If you see significant numbers here, you've found a cost optimization opportunity.

### Query 2: Top 5 AWS Accounts Generating S3 Traffic

Now let's identify which accounts are the biggest culprits:

```sql
SELECT tgw_src_vpc_account_id, 
       ROUND(SUM(bytes / 1073741824.0), 2) AS total_gbytes
FROM "default"."vpc_flow_logs_tgw_attachment_outbound"
WHERE pkt_dst_aws_service = 'S3'
GROUP BY tgw_src_vpc_account_id
ORDER BY total_gbytes DESC
LIMIT 5;
```

This query will show you which AWS accounts are generating the most S3 traffic through the NAT Gateway. The results might surprise you—sometimes a single misconfigured application can generate terabytes of unnecessary traffic.

## Advanced Analysis Techniques

### Account Name Mapping

Raw account IDs aren't very helpful for humans, right? Let's make our data more readable by creating a mapping table. First, generate the mapping data:

```bash
aws organizations list-accounts \
  --query 'Accounts[*].[Id,Name]' \
  --output json | jq -r '.[] | @csv' > account_mapping.csv
```

Upload this CSV file to an S3 bucket, then create an Athena table:

```sql
CREATE EXTERNAL TABLE aws_account_mapping (
  account_id STRING,
  account_name STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'skip.header.line.count' = '1'
)
LOCATION 's3://your-bucket/account-mapping/';
```

Now you can join this with your flow logs for more readable results:

```sql
SELECT f.tgw_src_vpc_account_id,
       a.account_name,
       ROUND(SUM(f.bytes / 1073741824.0), 2) AS total_gbytes
FROM "default"."vpc_flow_logs_tgw_attachment_outbound" f
LEFT JOIN aws_account_mapping a ON f.tgw_src_vpc_account_id = a.account_id
WHERE f.pkt_dst_aws_service = 'S3'
GROUP BY f.tgw_src_vpc_account_id, a.account_name
ORDER BY total_gbytes DESC
LIMIT 10;
```

### Detailed Resource Analysis

Want to dig deeper into specific accounts? Let's start with a comprehensive view of all AWS resources accessing S3 through the NAT Gateway:

```sql
SELECT *
FROM "default"."vpc_flow_logs_tgw_attachment_outbound"
WHERE pkt_dst_aws_service = 'S3'
  AND tgw_src_vpc_account_id = 'your-account-id'
LIMIT 100;
```

Among the fields returned, you'll find these particularly useful for identifying the source of traffic:

- **`tgw_src_vpc_id`**: Source VPC identifier - tells you which VPC the traffic originated from
- **`tgw_src_subnet_id`**: Source subnet identifier - narrows down to the specific subnet
- **`tgw_src_eni`**: Source Elastic Network Interface - the specific network interface generating traffic
- **`srcaddr`**: Source IP address - the exact IP address of the resource making S3 requests

For a more focused analysis, this aggregated query shows you exactly which resources are generating the most traffic:

```sql
SELECT tgw_src_vpc_id,
       tgw_src_subnet_id,
       srcaddr,
       ROUND(SUM(bytes / 1073741824.0), 2) AS total_gbytes
FROM "default"."vpc_flow_logs_tgw_attachment_outbound"
WHERE pkt_dst_aws_service = 'S3'
  AND tgw_src_vpc_account_id = 'your-account-id'
GROUP BY tgw_src_vpc_id, tgw_src_subnet_id, srcaddr
ORDER BY total_gbytes DESC
LIMIT 5;
```

This level of detail helps you pinpoint exactly which VPC, subnet, network interface, and even specific IP address is generating the most traffic. With this information, you can identify the exact resources that need S3 Gateway endpoints configured.

## Best Practices

### Cost Optimization Strategy

1. **Prioritize by Volume**: Focus on the accounts and VPCs generating the most traffic first
2. **Implement S3 Gateway Endpoints**: This is usually the fastest fix—create VPC endpoints for S3 in affected VPCs
3. **Monitor Regularly**: Set up this analysis as a monthly cost review process
4. **Automate Alerts**: Consider setting up CloudWatch alarms based on NAT Gateway data processing charges

### Query Performance Tips

- **Use Date Filters**: Always include date ranges in your WHERE clauses to limit data scanning
- **Leverage Partitions**: The partition projection we set up automatically optimizes query performance
- **Start Small**: When exploring data, use LIMIT clauses to avoid expensive full table scans

### Security Considerations

- **Data Sensitivity**: VPC Flow Logs contain IP addresses and network patterns—treat them as sensitive data
- **Access Control**: Ensure only authorized personnel can access Athena and the underlying S3 buckets
- **Retention Policies**: Consider implementing lifecycle policies for flow log data based on your compliance requirements

## Key Takeaways

After working through this lab, here are the most important points to remember:

1. **Hidden Costs Are Real**: S3 traffic through NAT Gateways can represent significant hidden costs in your AWS bill
2. **VPC Endpoints Are Your Friend**: S3 Gateway endpoints are free and can eliminate unnecessary NAT Gateway charges
3. **Data-Driven Decisions**: Using actual flow log data provides concrete evidence for optimization efforts
4. **Regular Monitoring**: This type of analysis should be part of your regular cost optimization process

The approach we've covered here is particularly powerful because it uses AWS's own data to identify optimization opportunities. There's something satisfying about using AWS tools to find ways to reduce your AWS costs, don't you think?

## Troubleshooting Common Issues

### Query Returns No Results
- **Check Data Location**: Verify your S3 path in the table definition
- **Verify Flow Logs**: Ensure VPC Flow Logs are actually enabled and generating data
- **Date Range**: Confirm your date projection range includes recent data

### Performance Issues
- **Add Date Filters**: Always filter by date to reduce data scanning
- **Check Partition Projection**: Ensure the date format matches your actual S3 structure
- **Query Complexity**: Break complex queries into simpler parts for testing

### Permission Errors
- **Athena Permissions**: Verify IAM permissions for Athena service
- **S3 Access**: Ensure Athena can read from your flow logs S3 bucket
- **Cross-Account Access**: If using multiple accounts, verify cross-account permissions

## Conclusion

Throughout this lab, you've learned to use Amazon Athena and VPC Flow Logs to identify S3 traffic unnecessarily flowing through NAT Gateways—a common source of hidden AWS costs.

The data-driven approach you've mastered here provides concrete evidence for optimization decisions, making it easier to justify implementing S3 Gateway endpoints. These same analytical techniques can be applied to other cost optimization scenarios across your AWS infrastructure.

Remember to make this analysis part of your regular cost review process. Network patterns evolve, and staying ahead of inefficiencies helps prevent small issues from becoming significant budget impacts.

## References

### AWS Documentation
- [VPC Flow Logs User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)
- [Amazon Athena User Guide](https://docs.aws.amazon.com/athena/latest/ug/what-is.html)
- [VPC Endpoints for Amazon S3](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)
- [Transit Gateway Flow Logs](https://docs.aws.amazon.com/vpc/latest/tgw/flow-logs.html)
- [How do I use Athena to analyze Amazon VPC flow logs?](https://repost.aws/knowledge-center/athena-analyze-vpc-flow-logs)

### Cost Optimization Resources
- [AWS Cost Optimization Best Practices](https://aws.amazon.com/aws-cost-management/cost-optimization/)
- [VPC Endpoint Pricing](https://aws.amazon.com/vpc/pricing/)
- [NAT Gateway Pricing](https://aws.amazon.com/vpc/pricing/)

### Additional Reading
- [AWS Well-Architected Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)
- [Athena Query Performance Tuning](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning.html)
- [AWS Organizations API Reference](https://docs.aws.amazon.com/organizations/latest/APIReference/Welcome.html)