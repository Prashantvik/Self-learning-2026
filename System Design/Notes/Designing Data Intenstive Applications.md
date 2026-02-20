# Designing Data-Intensive Applications Notes

## Chapter 1: Reliable, Scalable, and Maintainable Applications

### Key Concepts

**Data-Intensive vs Compute-Intensive Applications**
- Modern apps are often limited by data (amount, complexity, change rate) rather than CPU
- Raw CPU power rarely the limiting factor anymore

### Three Pillars of Data Systems

#### 1. Reliability
- **Definition**: System continues working correctly even when things go wrong
- **Types of Faults**:
  - Hardware faults (disk crashes, RAM failure, power outages)
  - Software errors (bugs, cascading failures, runaway processes)
  - Human errors (configuration mistakes, operational errors)
- **Approaches**: 
  - Redundancy and failover
  - Fault tolerance over fault prevention
  - Design for failure scenarios

#### 2. Scalability
- **Definition**: Ability to handle increased load gracefully
- **Load Parameters**: 
  - Requests per second
  - Read/write ratio
  - Concurrent users
  - Data volume
- **Performance Metrics**:
  - Throughput (requests per second)
  - Response time (latency)
  - Percentiles (p50, p95, p99, p999)
- **Scaling Approaches**:
  - Vertical scaling (scale up) - more powerful machines
  - Horizontal scaling (scale out) - more machines
  - Elastic scaling - automatic resource adjustment

#### 3. Maintainability
- **Definition**: System should be easy to operate, understand, and modify
- **Key Aspects**:
  - **Operability**: Easy for ops teams to run smoothly
  - **Simplicity**: Easy for new engineers to understand
  - **Evolvability**: Easy to adapt to changing requirements

### Important Principles

**Fault vs Failure**
- Fault: One component deviating from spec
- Failure: System as a whole stops providing service
- Build fault-tolerant systems to prevent faults from causing failures

**Load Testing**
- Use realistic load parameters
- Focus on percentiles, not just averages
- Consider tail latencies (p99, p999)

**Complexity Management**
- Avoid accidental complexity
- Use appropriate abstractions
- Modular design for evolvability

### Real-World Examples Mentioned
- Twitter's home timeline scaling challenges
- Fanout approaches for social media feeds
- Load balancing strategies

### Key Takeaways
1. Most modern applications are data-intensive, not compute-intensive
2. Reliability, scalability, and maintainability are fundamental requirements
3. Design systems to handle faults gracefully
4. Use percentiles to measure performance realistically
5. Keep systems simple and evolvable for long-term success

---

## Chapter 2: Data Models and Query Languages

### Data Model Evolution
**Hierarchy of Abstractions**:
1. Application code → Data structures/APIs
2. Data structures → General-purpose data model (JSON, XML, tables, graph)
3. Data model → Database engine storage (bytes in memory/disk)
4. Hardware → Machine code representation

### Three Main Data Models

#### 1. Relational Model (SQL)
- **Structure**: Tables with rows and columns
- **Strengths**: 
  - ACID transactions
  - Powerful query language (SQL)
  - Well-understood
  - Strong consistency
- **Use Cases**: Traditional business applications, complex queries

**Example**:
```sql
-- User profile with multiple emails
SELECT u.name, e.email 
FROM users u 
JOIN emails e ON u.id = e.user_id 
WHERE u.region = 'US';
```

#### 2. Document Model (NoSQL)
- **Structure**: Self-contained documents (JSON, XML)
- **Strengths**:
  - Schema flexibility
  - Better locality for nested data
  - Closer to application objects
- **Weaknesses**: Limited join support, weaker consistency

**Example**:
```json
// User profile document
{
  "user_id": 251,
  "name": "Bill Gates",
  "region": "US",
  "emails": [
    "bill@microsoft.com",
    "bill@gates.foundation"
  ],
  "positions": [
    {
      "job_title": "Co-chair",
      "organization": "Bill & Melinda Gates Foundation"
    }
  ]
}
```

#### 3. Graph Model
- **Structure**: Vertices (entities) and edges (relationships)
- **Types**:
  - Property graphs (Neo4j)
  - Triple-store (RDF)
- **Use Cases**: Complex many-to-many relationships, recommendations, fraud detection

**Example**:
```cypher
// Find people who like the same things as user
MATCH (user:Person {name: "Alice"})-[:LIKES]->(thing)<-[:LIKES]-(other:Person)
RETURN other.name, COUNT(thing) as common_interests
ORDER BY common_interests DESC
```

### Key Concepts

#### Schema Flexibility
- **Schema-on-write** (Relational): Schema enforced when data is written
- **Schema-on-read** (Document): Schema interpreted when data is read

**Example Comparison**:
```sql
-- Relational: Must alter schema first
ALTER TABLE users ADD COLUMN middle_name VARCHAR(50);
```
```json
// Document: Just start including the field
{
  "name": "John",
  "middle_name": "William",  // New field added naturally
  "email": "john@example.com"
}
```

#### Data Locality
- **Document databases**: Related data stored together
- **Relational**: May require multiple table lookups

**Example**:
```javascript
// Document: Single read operation
db.users.findOne({user_id: 251}) // Gets all user data at once

// vs Relational: Multiple queries needed
SELECT * FROM users WHERE id = 251;
SELECT * FROM emails WHERE user_id = 251;
SELECT * FROM positions WHERE user_id = 251;
```

### Query Languages

#### Declarative vs Imperative
- **Declarative** (SQL): Specify what you want, not how to get it
- **Imperative**: Specify exact steps to follow

**Example**:
```sql
-- Declarative (SQL)
SELECT * FROM animals WHERE family = 'Sharks';
```
```javascript
// Imperative (JavaScript)
function getSharks(animals) {
    var sharks = [];
    for (var i = 0; i < animals.length; i++) {
        if (animals[i].family === "Sharks") {
            sharks.push(animals[i]);
        }
    }
    return sharks;
}
```

#### MapReduce Querying
**Example in MongoDB**:
```javascript
// Count animals by family
db.animals.mapReduce(
    function map() { emit(this.family, 1); },
    function reduce(key, values) { return Array.sum(values); },
    { out: "family_counts" }
);
```

### Real-World Examples

**LinkedIn Profile Storage**:
- **Document approach**: Store entire profile as one document
- **Relational approach**: Normalize into users, positions, educations, skills tables

**Facebook Social Graph**:
- **Graph database**: Users, pages, posts as vertices; friendships, likes, comments as edges
- Natural fit for "friends of friends" queries

**E-commerce Product Catalog**:
- **Document**: Flexible schema for different product types
- **Relational**: Fixed schema requires complex joins for varied attributes

### Choosing the Right Model

| Use Case | Best Model | Reason |
|----------|------------|---------|
| Financial transactions | Relational | ACID compliance needed |
| Content management | Document | Flexible schema, data locality |
| Social networks | Graph | Complex relationships |
| Analytics/Reporting | Relational | Complex aggregations |
| Real-time personalization | Document/Graph | Fast reads, flexible structure |

### Key Takeaways
1. **No one-size-fits-all**: Each model has specific strengths
2. **Application shape matters**: Choose model that matches your data access patterns
3. **Polyglot persistence**: Many systems use multiple data models
4. **Schema evolution**: Consider how your data structure will change over time
5. **Query complexity**: Match query language power to your needs