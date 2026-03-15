---
name: dev-engineering-super-skill
description: Comprehensive full-stack development and engineering skill merging Perplexity Computer's built-in dev tools with Claude Code's engineering team skills. Covers architecture, frontend, backend, fullstack, QA/testing, DevOps/CI-CD, security, debugging, TDD, code review, and more. Use when writing code, debugging, architecting systems, reviewing code, writing tests, deploying, or doing any software engineering work.
license: MIT
metadata:
  author: get-zeked
  version: '1.0'
---

# Dev & Engineering Super-Skill

Comprehensive engineering operations manual merging Perplexity Computer's built-in data/web capabilities with Claude Code's full engineering team skill set. Covers every phase of the software development lifecycle.

---

## Table of Contents

1. [Gap Analysis — Perplexity vs Claude Code Skills](#section-1-gap-analysis)
2. [Architecture & System Design](#section-2-architecture--system-design)
3. [Frontend Engineering](#section-3-frontend-engineering)
4. [Backend Engineering](#section-4-backend-engineering)
5. [Fullstack Development](#section-5-fullstack-development)
6. [Testing & Quality Assurance](#section-6-testing--quality-assurance)
7. [Debugging & Code Review](#section-7-debugging--code-review)
8. [DevOps & CI/CD](#section-8-devops--cicd)
9. [Security Engineering](#section-9-security-engineering)
10. [Data Engineering & Analysis](#section-10-data-engineering--analysis)
11. [Changelog & Documentation](#section-11-changelog--documentation)
12. [Unique Perplexity Computer Capabilities](#section-12-unique-perplexity-computer-capabilities)

---

## Section 1: Gap Analysis

### Capability Comparison Matrix

| Capability | Perplexity Computer Built-in | Claude Code (Engineering Skills) | Merged Super-Skill Coverage |
|------------|------------------------------|-----------------------------------|-----------------------------|
| SQL (Snowflake, BigQuery, PG, Databricks) | `sql-queries` skill | Backend SQL patterns | **Full: multi-dialect SQL + optimization** |
| Data profiling & exploration | `data-exploration` skill | — | **Full: profiling, nulls, outliers, quality** |
| Data validation & QA methodology | `data-validation` skill | QA/Testing patterns | **Full: both code and data validation** |
| Visualization (matplotlib, seaborn, plotly) | `data-visualization` skill | — | **Full: chart selection + accessibility** |
| Statistical analysis | `statistical-analysis` skill | — | **Full: hypothesis testing, distributions** |
| Website/web app/web game building | `website-building` skill | Frontend/Fullstack | **Full: design system + React + Next.js** |
| Server-side logic, CGI, webhooks | `webserver` skill | Backend engineer | **Full: CGI + FastAPI + Express** |
| Architecture diagrams (Mermaid, PlantUML) | — | `senior-architect` | **Full: C4, sequence, component, layer** |
| Dependency analysis | — | `senior-architect` | **Full: circular deps, coupling scores** |
| ADR creation | — | `senior-architect` | **Full: decision records + workflows** |
| React/Next.js frontend | — | `senior-frontend` | **Full: hooks, Server Components, bundles** |
| Bundle optimization | — | `senior-frontend` | **Full: heavy dep detection + alternates** |
| REST/GraphQL API design | — | `senior-backend` | **Full: OpenAPI, scaffolding, load testing** |
| Database migration tooling | — | `senior-backend` | **Full: schema diff + rollback** |
| Test suite generation | — | `senior-qa` | **Full: RTL, Playwright, coverage gaps** |
| E2E testing (Playwright/Cypress) | — | `senior-qa` | **Full: route scaffolding + Page Objects** |
| TDD methodology | — | `tdd-guide` + obra TDD | **Full: Red-Green-Refactor + Iron Law** |
| CI/CD pipeline generation | — | `senior-devops` | **Full: GitHub Actions, CircleCI, Terraform** |
| Security scanning (SAST/secrets) | — | `senior-secops` | **Full: code scan + CVE assessment** |
| Compliance checking (SOC2, GDPR, HIPAA) | — | `senior-secops` | **Full: automated compliance verification** |
| Threat modeling (STRIDE) | — | `senior-security` | **Full: DREAD scoring + DFD analysis** |
| Code review automation | — | `code-reviewer` | **Full: PR analysis + quality checker** |
| Systematic debugging | — | obra systematic-debugging | **Full: 4-phase root cause analysis** |
| Changelog from git commits | — | `changelog-generator` | **Full: commit-to-release-notes pipeline** |
| Live web research for docs | **Yes — real-time** | No training cutoff workaround | **Perplexity exclusive** |
| AI image generation (mockups) | **Yes** | No | **Perplexity exclusive** |
| 400+ app integrations | **Yes** | No | **Perplexity exclusive** |
| Deploy websites live | **Yes** | No | **Perplexity exclusive** |

### Unique to Perplexity Computer
- Real-time library/API documentation lookup
- Website deployment in minutes
- AI-generated UI mockups and design assets
- Scheduled deployment monitoring
- 400+ third-party service integrations

### Unique to Claude Code Engineering Skills
- Multi-phase systematic debugging (obra)
- Iron-law TDD enforcement
- PR complexity and risk scoring
- STRIDE/DREAD threat modeling
- Compliance automation (SOC2, PCI-DSS, HIPAA, GDPR)

### Merged Additions (Super-Skill Only)
- Data engineering + backend SQL in a unified workflow
- Website-building design system merged with React/Next.js patterns
- Perplexity web research applied to package/library decisions
- Statistical analysis informing data-layer design choices

---

## Section 2: Architecture & System Design

### When to Use This Section
- Designing new systems or refactoring existing architecture
- Making technology stack decisions
- Creating technical documentation, ADRs
- Evaluating microservices vs. monolith trade-offs

### Architecture Diagram Generator

Generate diagrams from your project structure in multiple formats.

```bash
# Mermaid (default, renders in GitHub/Notion)
python scripts/architecture_diagram_generator.py ./project --format mermaid --type component

# PlantUML (enterprise docs)
python scripts/architecture_diagram_generator.py ./project --format plantuml --type layer

# ASCII (terminal-friendly)
python scripts/architecture_diagram_generator.py ./project --format ascii

# Save to file
python scripts/architecture_diagram_generator.py ./project -o architecture.md
```

**Diagram Types:**
| Type | Use Case |
|------|----------|
| `component` | Modules and their relationships |
| `layer` | Presentation / Business / Data layers |
| `deployment` | Physical/cloud deployment topology |
| `sequence` | Request flow across services |

**Example Mermaid Output:**
```mermaid
graph TD
    A[API Gateway] --> B[Auth Service]
    A --> C[User Service]
    B --> D[(PostgreSQL)]
    C --> D
    C --> E[Redis Cache]
```

### C4 Model Diagrams

```mermaid
C4Context
    title System Context — E-Commerce Platform
    Person(customer, "Customer", "Browses and purchases products")
    System(ecommerce, "E-Commerce Platform", "Handles orders, payments, inventory")
    System_Ext(payment, "Stripe", "Payment processing")
    System_Ext(email, "SendGrid", "Transactional email")
    Rel(customer, ecommerce, "Uses", "HTTPS")
    Rel(ecommerce, payment, "Charges", "HTTPS/API")
    Rel(ecommerce, email, "Sends via", "HTTPS/API")
```

### Dependency Analyzer

```bash
# Full dependency report
python scripts/dependency_analyzer.py ./project --verbose

# JSON output for CI/CD integration
python scripts/dependency_analyzer.py ./project --output json

# Check only circular dependencies
python scripts/dependency_analyzer.py ./project --check circular

# Supported package managers: npm/yarn, pip/pyproject, go.mod, Cargo.toml
```

**Sample Output:**
```
Dependency Analysis Report
==========================
Total dependencies: 47 (32 direct, 15 transitive)
Coupling score: 72/100 (moderate)

Issues found:
- CIRCULAR: auth → user → permissions → auth
- OUTDATED: lodash 4.17.15 → 4.17.21 (security)

Recommendations:
1. Extract shared interface to break circular dependency
2. Update lodash to fix CVE-2020-8203
```

### Architecture Decision Records (ADRs)

Use ADRs to document significant technical decisions. Store in `docs/adr/`.

**ADR Template:**
```markdown
# ADR-001: Choose PostgreSQL as Primary Database

**Status:** Accepted
**Date:** 2026-03-03
**Deciders:** Engineering Team

## Context
We need a database for our SaaS application handling 500K users.

## Decision
Use PostgreSQL 16 as the primary relational database.

## Consequences
- Strong ACID compliance for financial data
- Excellent full-text search with pg_trgm
- Requires DBA knowledge for tuning at scale
- Well-supported by Prisma, Drizzle, SQLAlchemy
```

### Architecture Pattern Selection

**Step 1 — Assess team and project size:**

| Team Size | Recommended Starting Point |
|-----------|---------------------------|
| 1–3 developers | Modular monolith |
| 4–10 developers | Modular monolith or service-oriented |
| 10+ developers | Consider microservices |

**Step 2 — Match pattern to requirements:**

| Requirement | Recommended Pattern |
|-------------|-------------------|
| Rapid MVP | Modular Monolith |
| Independent team deployment | Microservices |
| Complex domain logic | Domain-Driven Design |
| High read/write ratio difference | CQRS |
| Audit trail required | Event Sourcing |
| Third-party integrations | Hexagonal/Ports & Adapters |

**Step 3 — Database selection:**

```
PostgreSQL → Default choice for most applications
MongoDB    → Document store, flexible schema
Redis      → Caching, sessions, real-time features
DynamoDB   → Serverless, auto-scaling, AWS-native
TimescaleDB → Time-series data with SQL interface
```

**Scale thresholds:**
- < 1M records, single region → PostgreSQL or MySQL
- 1M–100M records, read-heavy → PostgreSQL with read replicas
- > 100M records, global → CockroachDB, Spanner, or DynamoDB
- High write throughput (> 10K/sec) → Cassandra or ScyllaDB

### Monolith vs Microservices Decision

**Choose Monolith when:**
- [ ] Team is small (< 10 developers)
- [ ] Domain boundaries are unclear
- [ ] Rapid iteration is priority
- [ ] Shared database is acceptable

**Choose Microservices when:**
- [ ] Teams can own services end-to-end
- [ ] Independent deployment is critical
- [ ] Different scaling requirements per component
- [ ] Domain boundaries are well understood

**Hybrid approach:** Start with a modular monolith. Extract services only when a module has significantly different scaling needs, a team needs independent deployment, or technology constraints require separation.

### Architecture Assessment Tool

```bash
# Full assessment
python scripts/project_architect.py ./project --verbose

# JSON output
python scripts/project_architect.py ./project --output json

# Check specific aspect
python scripts/project_architect.py ./project --check layers
```

**Sample Output:**
```
Architecture Assessment
=======================
Detected pattern: Layered Architecture (confidence: 85%)

  ✓ controllers/  - Presentation layer detected
  ✓ services/     - Business logic layer detected
  ✓ repositories/ - Data access layer detected
  ⚠ models/       - Mixed domain and DTOs

Issues:
- LARGE FILE: UserService.ts (1,847 lines) - consider splitting
- MIXED CONCERNS: PaymentController contains business logic

Recommendations:
1. Split UserService into focused services
2. Move business logic from controllers to services
3. Separate domain models from DTOs
```

### System Design Workflows

**Capacity Planning Checklist:**
- [ ] Estimate daily active users and peak concurrency
- [ ] Calculate storage growth rate (12 months)
- [ ] Identify read/write ratio per service
- [ ] Define SLAs (p50/p95/p99 latency targets)
- [ ] Plan for 3x headroom above expected peak

**API Design Checklist:**
- [ ] Define resources and operations (OpenAPI first)
- [ ] Establish versioning strategy (`/v1/`, header-based)
- [ ] Define error response format (consistent across all endpoints)
- [ ] Design pagination (cursor-based for large datasets)
- [ ] Document authentication/authorization model

---

## Section 3: Frontend Engineering

### When to Use This Section
- Building React/Next.js components or pages
- Optimizing bundle size or Core Web Vitals
- Implementing accessibility and responsive design
- Setting up a new frontend project

### Project Scaffolding

```bash
# Next.js 14+ with App Router
python scripts/frontend_scaffolder.py my-app --template nextjs

# React + Vite
python scripts/frontend_scaffolder.py my-app --template react

# With features
python scripts/frontend_scaffolder.py dashboard --template nextjs --features auth,api,forms,testing

# Preview without creating files
python scripts/frontend_scaffolder.py my-app --template nextjs --dry-run
```

**Generated Next.js Structure:**
```
my-app/
├── app/
│   ├── layout.tsx        # Root layout with fonts
│   ├── page.tsx          # Home page
│   ├── globals.css       # Tailwind + CSS variables
│   └── api/health/route.ts
├── components/
│   ├── ui/               # Button, Input, Card
│   └── layout/           # Header, Footer, Sidebar
├── hooks/                # useDebounce, useLocalStorage
├── lib/                  # utils (cn), constants
├── types/                # TypeScript interfaces
├── tailwind.config.ts
├── next.config.js
└── package.json
```

### Component Generation

```bash
# Client component (default)
python scripts/component_generator.py Button --dir src/components/ui

# Server component
python scripts/component_generator.py ProductCard --type server

# With test and Storybook story
python scripts/component_generator.py UserProfile --with-test --with-story

# Custom hook
python scripts/component_generator.py FormValidation --type hook

# Preview without creating
python scripts/component_generator.py Button --dry-run
```

**Generated Component Pattern:**
```tsx
'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  disabled?: boolean;
  className?: string;
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({ variant = 'primary', disabled, className, children, onClick }: ButtonProps) {
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={cn(
        'px-4 py-2 rounded font-medium transition-colors',
        variant === 'primary' && 'bg-blue-600 text-white hover:bg-blue-700',
        variant === 'secondary' && 'bg-gray-100 text-gray-900 hover:bg-gray-200',
        variant === 'ghost' && 'text-gray-700 hover:bg-gray-100',
        disabled && 'opacity-50 cursor-not-allowed',
        className
      )}
    >
      {children}
    </button>
  );
}
```

### React Patterns

**Compound Components — share state between related components:**
```tsx
const Tabs = ({ children, defaultTab = 0 }) => {
  const [active, setActive] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      {children}
    </TabsContext.Provider>
  );
};

Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage
<Tabs>
  <Tabs.List>
    <Tabs.Tab>Overview</Tabs.Tab>
    <Tabs.Tab>Details</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel>Overview content</Tabs.Panel>
  <Tabs.Panel>Details content</Tabs.Panel>
</Tabs>
```

**Custom Hooks — extract reusable logic:**
```tsx
function useDebounce<T>(value: T, delay = 500): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
const debouncedSearch = useDebounce(searchTerm, 300);
```

**Generic Components with TypeScript:**
```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
  emptyState?: React.ReactNode;
}

function List<T>({ items, renderItem, keyExtractor, emptyState }: ListProps<T>) {
  if (items.length === 0) return <>{emptyState}</>;
  return (
    <ul>
      {items.map((item, i) => (
        <li key={keyExtractor(item)}>{renderItem(item, i)}</li>
      ))}
    </ul>
  );
}
```

### Next.js Optimization

**Server vs Client Components Decision:**

Use Server Components by default. Add `'use client'` only when you need:
- Event handlers (onClick, onChange)
- State (useState, useReducer)
- Effects (useEffect)
- Browser APIs (window, localStorage)

```tsx
// Server Component (default) — no 'use client'
async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);  // Server-side fetch, no waterfall

  return (
    <div>
      <h1>{product.name}</h1>
      <AddToCartButton productId={product.id} />  {/* Client island */}
    </div>
  );
}

// Client Component
'use client';
function AddToCartButton({ productId }: { productId: string }) {
  const [adding, setAdding] = useState(false);
  return (
    <button
      onClick={async () => {
        setAdding(true);
        await addToCart(productId);
        setAdding(false);
      }}
      disabled={adding}
    >
      {adding ? 'Adding...' : 'Add to Cart'}
    </button>
  );
}
```

**Parallel Data Fetching:**
```tsx
async function Dashboard() {
  // Fetch in parallel, not waterfall
  const [user, stats, notifications] = await Promise.all([
    getUser(),
    getStats(),
    getNotifications(),
  ]);
  return <div>...</div>;
}
```

**Streaming with Suspense:**
```tsx
async function ProductPage({ params }: { params: { id: string } }) {
  return (
    <div>
      <ProductDetails id={params.id} />  {/* Loads first */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={params.id} />  {/* Streams in */}
      </Suspense>
    </div>
  );
}
```

**Next.js Config:**
```js
// next.config.js
const nextConfig = {
  images: {
    remotePatterns: [{ hostname: 'cdn.example.com' }],
    formats: ['image/avif', 'image/webp'],
  },
  experimental: {
    optimizePackageImports: ['lucide-react', '@heroicons/react'],
  },
};
```

### Bundle Analysis

```bash
# Analyze bundle
python scripts/bundle_analyzer.py /path/to/project

# Verbose — check import patterns
python scripts/bundle_analyzer.py . --verbose
```

**Bundle Score Interpretation:**

| Score | Grade | Action |
|-------|-------|--------|
| 90–100 | A | Well-optimized |
| 80–89 | B | Minor optimizations available |
| 70–79 | C | Replace heavy dependencies |
| 60–69 | D | Multiple issues need attention |
| < 60 | F | Critical bundle size problems |

**Heavy Dependency Replacements:**

| Package | Size | Alternative |
|---------|------|-------------|
| moment | 290KB | date-fns (12KB) or dayjs (2KB) |
| lodash | 71KB | lodash-es with tree-shaking |
| axios | 14KB | Native fetch or ky (3KB) |
| jquery | 87KB | Native DOM APIs |
| @mui/material | Large | shadcn/ui or Radix UI |

### CSS/Tailwind Design System

```tsx
// Conditional classes with cn() utility
import { cn } from '@/lib/utils';

// CSS variables for theming
:root {
  --color-primary: #3B82F6;
  --color-surface: #FFFFFF;
  --color-text: #1F2937;
  --spacing-base: 0.25rem;
  --radius-base: 0.375rem;
}

// Tailwind component
<button className={cn(
  // Base
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  // Size
  size === 'sm' && 'h-8 px-3 text-xs',
  size === 'md' && 'h-10 px-4 text-sm',
  size === 'lg' && 'h-12 px-6 text-base',
  // Variant
  variant === 'primary' && 'bg-blue-600 text-white hover:bg-blue-700',
  variant === 'outline' && 'border border-gray-200 hover:bg-gray-50',
  // State
  disabled && 'pointer-events-none opacity-50'
)} />
```

**Typography Scale:**
```css
/* Fluid type scale */
--font-xs:   clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
--font-sm:   clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
--font-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
--font-lg:   clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
--font-xl:   clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
--font-2xl:  clamp(1.5rem, 1.3rem + 1vw, 2rem);
```

### Accessibility Checklist

- [ ] Semantic HTML: Use `<button>`, `<nav>`, `<main>`, `<article>`, `<section>`
- [ ] Keyboard Navigation: All interactive elements are keyboard-reachable
- [ ] ARIA Labels: Provide labels for icons and complex widgets
- [ ] Color Contrast: Minimum 4.5:1 for normal text, 3:1 for large text
- [ ] Focus Indicators: Visible, high-contrast focus rings
- [ ] Skip Links: "Skip to main content" for keyboard users
- [ ] Alt Text: Meaningful descriptions for all images
- [ ] Form Labels: All inputs have associated `<label>` elements

```tsx
// Accessible icon button
<button
  type="button"
  aria-label="Close dialog"
  onClick={onClose}
  className="focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:outline-none rounded"
>
  <XIcon aria-hidden="true" />
</button>

// Skip link
<a href="#main-content" className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4">
  Skip to main content
</a>
```

### SEO Optimization

```tsx
// app/layout.tsx — root metadata
export const metadata: Metadata = {
  title: { template: '%s | My App', default: 'My App' },
  description: 'Application description for SEO',
  openGraph: {
    type: 'website',
    url: 'https://example.com',
    images: [{ url: '/og-image.png', width: 1200, height: 630 }],
  },
};

// Per-page metadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const product = await getProduct(params.id);
  return {
    title: product.name,
    description: product.description,
  };
}
```

---

## Section 4: Backend Engineering

### When to Use This Section
- Designing REST or GraphQL APIs
- Optimizing database queries and migrations
- Implementing authentication and authorization
- Load testing and performance tuning

### API Scaffolding

```bash
# Generate Express routes from OpenAPI spec
python scripts/api_scaffolder.py openapi.yaml --framework express --output src/routes/

# Generate from database schema
python scripts/api_scaffolder.py --from-db postgres://localhost/mydb --output src/routes/

# Generate OpenAPI spec from existing routes
python scripts/api_scaffolder.py src/routes/ --generate-spec --output openapi.yaml

# Frameworks: express, fastify, koa
```

### API Design Patterns

**OpenAPI-First Workflow:**
```yaml
# openapi.yaml
openapi: 3.0.3
info:
  title: User Service API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: cursor
          in: query
          schema: { type: string }
        - name: limit
          in: query
          schema: { type: integer, default: 20, maximum: 100 }
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
```

**Standard Response Format:**
```json
{
  "data": { "id": "usr_123", "email": "user@example.com" },
  "meta": { "requestId": "req_abc123", "timestamp": "2026-03-03T09:00:00Z" }
}
```

**Standard Error Format:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [{ "field": "email", "message": "must be a valid email address" }]
  },
  "meta": { "requestId": "req_abc123" }
}
```

**HTTP Status Codes:**
| Code | Use Case |
|------|----------|
| 200 | Success (GET, PUT, PATCH) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Validation error |
| 401 | Authentication required |
| 403 | Permission denied |
| 404 | Resource not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

### Database Design & Optimization

```bash
# Analyze schema performance
python scripts/database_migration_tool.py --connection $DATABASE_URL --analyze

# Generate migration from schema diff
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --compare schema/v2.sql --output migrations/

# Dry-run migration
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --migrate migrations/20260303_add_indexes.sql --dry-run

# Apply migration
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --migrate migrations/20260303_add_indexes.sql
```

**Database Index Strategy:**
```sql
-- Single column (equality lookups)
CREATE INDEX idx_users_email ON users(email);

-- Composite (multi-column queries — order matters)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial (filtered subsets)
CREATE INDEX idx_orders_active ON orders(created_at) WHERE status = 'active';

-- Covering (avoid table lookup entirely)
CREATE INDEX idx_users_email_name ON users(email) INCLUDE (name);

-- Explain a slow query
EXPLAIN ANALYZE SELECT * FROM orders
WHERE user_id = 123
ORDER BY created_at DESC
LIMIT 10;
-- Look for: "Seq Scan" (bad), "Index Scan" (good)
```

**N+1 Query Prevention:**
```typescript
// BAD: N+1
const users = await db.user.findMany();
for (const user of users) {
  const orders = await db.order.findMany({ where: { userId: user.id } });
}

// GOOD: Eager loading with Prisma
const users = await db.user.findMany({
  include: {
    orders: {
      where: { status: 'active' },
      orderBy: { createdAt: 'desc' },
      take: 10,
    },
  },
});
```

**Connection Pooling:**
```typescript
// PgBouncer or Prisma connection pool
const prisma = new PrismaClient({
  datasources: {
    db: { url: process.env.DATABASE_URL },
  },
  // Connection pool size: (2 * CPU cores) + 1
});

// Supabase / NeonDB pooled connection
DATABASE_URL="postgresql://user:pass@host:6543/db?pgbouncer=true&connection_limit=10"
```

### Authentication & Authorization

```typescript
// JWT configuration
const jwtConfig = {
  secret: process.env.JWT_SECRET,   // Must be from env, never hardcoded
  expiresIn: '15m',                 // Short-lived access tokens
  algorithm: 'RS256' as const,      // Prefer asymmetric
};

// Password hashing
import bcrypt from 'bcrypt';
const SALT_ROUNDS = 12;
const hash = await bcrypt.hash(password, SALT_ROUNDS);
const match = await bcrypt.compare(password, hash);

// Rate limiting
import rateLimit from 'express-rate-limit';
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
});
app.use('/api/', apiLimiter);

// Input validation with Zod
import { z } from 'zod';
const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100),
  password: z.string().min(12).regex(/[A-Z]/).regex(/[0-9]/),
});
const data = CreateUserSchema.parse(req.body);
```

### API Load Testing

```bash
# Basic load test
python scripts/api_load_tester.py https://api.example.com/users \
  --concurrency 50 --duration 30

# POST with body and headers
python scripts/api_load_tester.py https://api.example.com/orders \
  --method POST \
  --header "Authorization: Bearer token123" \
  --body '{"product_id": 1, "quantity": 2}' \
  --concurrency 100 --duration 60

# Compare two API versions
python scripts/api_load_tester.py \
  https://api.example.com/v1/users \
  https://api.example.com/v2/users \
  --compare --concurrency 50 --duration 30
```

**Performance Targets:**
| Metric | Target |
|--------|--------|
| P50 latency | < 50ms |
| P95 latency | < 200ms |
| P99 latency | < 500ms |
| Error rate | < 0.1% |
| Throughput | > 500 req/s per instance |

### Server-Side Logic: CGI, Webhooks, SQLite

For lightweight server-side use cases (webhooks, form backends, data persistence):

```python
# Simple webhook receiver (CGI)
#!/usr/bin/env python3
import sys, json, hmac, hashlib, os

def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = 'sha256=' + hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

# SQLite backend for lightweight persistence
import sqlite3

def get_db():
    db = sqlite3.connect('data.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                message TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
```

### Security Hardening Workflow

```typescript
// Security headers with Helmet
import helmet from 'helmet';
app.use(helmet({
  contentSecurityPolicy: true,
  crossOriginEmbedderPolicy: true,
  hsts: { maxAge: 31536000, includeSubDomains: true },
}));

// CORS configuration
import cors from 'cors';
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || [],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
}));
```

---

## Section 5: Fullstack Development

### When to Use This Section
- Starting a new full-stack project from scratch
- Auditing an existing codebase for quality issues
- Choosing between tech stacks
- Setting up development workflows

### Project Scaffolding

```bash
# List available templates
python scripts/project_scaffolder.py --list-templates

# Next.js 14+ (App Router, TypeScript, Tailwind)
python scripts/project_scaffolder.py nextjs my-saas-app

# FastAPI + React + PostgreSQL
python scripts/project_scaffolder.py fastapi-react my-api

# MERN stack
python scripts/project_scaffolder.py mern my-project

# Django + React
python scripts/project_scaffolder.py django-react my-app

# JSON output for CI integration
python scripts/project_scaffolder.py nextjs my-app --json
```

**Generated Files Include:**
- Project structure with all necessary files
- `package.json` / `requirements.txt`
- TypeScript configuration (`tsconfig.json`)
- Docker and `docker-compose.yml`
- Environment file templates (`.env.example`)
- Next steps for running the project

### Code Quality Analysis

```bash
# Analyze current directory
python scripts/code_quality_analyzer.py .

# Verbose output with detailed findings
python scripts/code_quality_analyzer.py . --verbose

# JSON output
python scripts/code_quality_analyzer.py . --json

# Save report to file
python scripts/code_quality_analyzer.py . --output report.json
```

**Sample Output:**
```
CODE QUALITY ANALYSIS REPORT
============================================================
Overall Score: 75/100 (Grade: C)
Files Analyzed: 45
Total Lines: 12,500

--- SECURITY ---
  Critical: 1
  High: 2
  Medium: 5

--- COMPLEXITY ---
  Average Complexity: 8.5
  High Complexity Files: 3

--- RECOMMENDATIONS ---
1. [P0] SECURITY
   Issue: Potential hardcoded secret detected
   Action: Remove or secure sensitive data at line 42
```

### Stack Decision Matrix

| Requirement | Recommendation |
|-------------|---------------|
| SEO-critical site | Next.js with SSR |
| Internal dashboard | React + Vite |
| API-first backend | FastAPI or Fastify |
| Enterprise scale | NestJS + PostgreSQL |
| Rapid prototype | Next.js API routes |
| Document-heavy data | MongoDB |
| Complex queries | PostgreSQL |
| Real-time features | WebSockets + Redis Pub/Sub |
| Mobile app | React Native or Flutter |

### Development Workflow

**Git Workflow (Trunk-Based Development):**
```bash
# Create feature branch
git checkout -b feat/add-user-authentication

# Conventional commits
git commit -m "feat(auth): add JWT refresh token rotation"
git commit -m "fix(api): handle expired token edge case"
git commit -m "test(auth): add refresh token tests"
git commit -m "docs: update authentication API reference"

# Squash merge to main
git checkout main
git merge --squash feat/add-user-authentication
git commit -m "feat(auth): add JWT refresh token rotation (#123)"
```

**Local Development:**
```bash
# Docker Compose for all services
docker-compose up -d postgres redis

# Install and run
npm install
cp .env.example .env.local
npm run dev

# Database setup
npx prisma migrate dev
npx prisma db seed
```

**Common Issues:**
| Issue | Solution |
|-------|----------|
| N+1 queries | Use DataLoader or eager loading |
| Slow builds | Check bundle size, lazy load |
| Auth complexity | Use Auth.js or Clerk |
| Type errors | Enable strict mode in tsconfig |
| CORS issues | Configure middleware properly |

---

## Section 6: Testing & Quality Assurance

### When to Use This Section
- Setting up testing infrastructure for a new project
- Generating test suites for existing components
- Analyzing coverage gaps
- Establishing TDD workflows

### The Iron Law of TDD

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over with TDD. No exceptions without your human partner's explicit permission.

### Red-Green-Refactor Cycle

**RED — Write a failing test:**
```typescript
// One behavior, clear name, tests real code (not mocks)
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```

**Verify RED — MANDATORY, never skip:**
```bash
npm test path/to/test.test.ts
# FAIL: retryOperation is not defined
# ✓ Test fails for the RIGHT reason (feature missing, not a typo)
```

**GREEN — Minimal code to pass:**
```typescript
// Simplest code that passes the test — no over-engineering
async function retryOperation<T>(fn: () => T | Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
  throw new Error('unreachable');
}
```

**Verify GREEN:**
```bash
npm test path/to/test.test.ts
# PASS ✓
```

**REFACTOR — Clean up while staying green:**
- Remove duplication
- Improve names
- Extract helpers
- Do NOT add behavior

**TDD Verification Checklist — before marking work complete:**
- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for the expected reason
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] No console errors or warnings
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

**Common Rationalizations — all wrong:**
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll write tests after" | Tests passing immediately prove nothing. |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "TDD slows me down" | TDD is faster than debugging production. |

### Testing Pyramid

```
        /\
       /E2E\          10% — Few, slow, high confidence
      /------\
     / Integ. \       20% — Service boundaries, DB queries
    /----------\
   /    Unit    \     70% — Fast, isolated, many
  /--------------\
```

**Coverage Targets:**
- Statements: ≥ 80%
- Branches: ≥ 80%
- Functions: ≥ 80%
- Lines: ≥ 80%
- Critical business logic: 100%

### Test Suite Generation

```bash
# Generate Jest + RTL tests for React components
python scripts/test_suite_generator.py src/components/ --output __tests__/

# Include accessibility tests
python scripts/test_suite_generator.py src/ --output __tests__/ --include-a11y

# Only generate for uncovered files
python scripts/test_suite_generator.py src/ --uncovered-only --output __tests__/

# Scan without generating
python scripts/test_suite_generator.py src/ --scan-only
```

**Generated Test Pattern:**
```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from '../src/components/Button';

describe('Button', () => {
  it('renders with label', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup();
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    await user.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop passed', () => {
    render(<Button disabled>Click</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### Coverage Analysis

```bash
# Generate coverage report
npm test -- --coverage --coverageReporters=json

# Analyze coverage gaps
python scripts/coverage_analyzer.py coverage/coverage-final.json --threshold 80

# Enforce threshold (exit 1 if below)
python scripts/coverage_analyzer.py coverage/ --threshold 80 --strict

# Generate HTML report
python scripts/coverage_analyzer.py coverage/ --format html --output report.html
```

### E2E Testing with Playwright

```bash
# Scaffold E2E tests from Next.js routes
python scripts/e2e_test_scaffolder.py src/app/ --output e2e/

# Include Page Object Model classes
python scripts/e2e_test_scaffolder.py src/app/ --output e2e/ --include-pom

# Specific routes only
python scripts/e2e_test_scaffolder.py src/app/ --routes "/login,/dashboard,/checkout"
```

**Generated Playwright Test:**
```typescript
import { test, expect } from '@playwright/test';

test.describe('Login page', () => {
  test('allows user to log in with valid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Sign in' }).click();

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Welcome back')).toBeVisible();
  });

  test('shows error with invalid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.getByLabel('Email').fill('wrong@example.com');
    await page.getByLabel('Password').fill('wrongpassword');
    await page.getByRole('button', { name: 'Sign in' }).click();

    await expect(page.getByRole('alert')).toContainText('Invalid credentials');
  });
});
```

**Authentication Fixture:**
```typescript
// e2e/fixtures/auth.ts
import { test as base } from '@playwright/test';

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.getByLabel('Email').fill('test@example.com');
    await page.getByLabel('Password').fill('password');
    await page.getByRole('button', { name: 'Sign in' }).click();
    await page.waitForURL('/dashboard');
    await use(page);
  },
});
```

### Multi-Framework Test Support

```bash
# Generate Pytest tests
python scripts/test_generator.py --input source.py --framework pytest

# Generate JUnit tests
python scripts/test_generator.py --input UserService.java --framework junit

# Convert from Jest to Pytest
python scripts/framework_adapter.py --from jest --to pytest

# Generate test fixtures
python scripts/fixture_generator.py --entity User --count 10 --format json
```

### Common Testing Patterns

**React Testing Library queries (in order of preference):**
```typescript
// 1. Accessible role (best)
screen.getByRole('button', { name: /submit/i })

// 2. Label text
screen.getByLabelText(/email address/i)

// 3. Placeholder
screen.getByPlaceholderText(/search/i)

// 4. Text content
screen.getByText(/welcome/i)

// 5. Test ID (last resort)
screen.getByTestId('custom-element')
```

**Async testing:**
```typescript
// Wait for element to appear
await screen.findByText(/loaded successfully/i);

// Wait for element to disappear
await waitForElementToBeRemoved(() => screen.queryByText(/loading/i));

// Wait for condition
await waitFor(() => {
  expect(mockFn).toHaveBeenCalledWith(expect.objectContaining({ id: '123' }));
});
```

**API mocking with MSW:**
```typescript
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  http.get('/api/users', () => {
    return HttpResponse.json([{ id: 1, name: 'John' }]);
  }),
  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: 2, ...body }, { status: 201 });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

**Jest configuration:**
```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterFramework: ['@testing-library/jest-dom'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
};
```

### Testing Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Testing mock behavior | Tests mocks, not real code | Use real implementations |
| Testing implementation details | Brittle, breaks on refactoring | Test observable behavior |
| `test('it works')` | Vague test name | Describe behavior: `test('returns 401 for expired token')` |
| Multiple assertions without context | Hard to diagnose failures | Use `describe` blocks, one behavior per test |
| Hard-coded sleeps (`setTimeout`) | Flaky tests | Use `waitFor` / condition polling |
| Shared mutable test state | Test ordering bugs | Reset state in `beforeEach` |

---

## Section 7: Debugging & Code Review

### When to Use This Section
- Encountering any bug, test failure, or unexpected behavior
- Reviewing pull requests
- Assessing code quality before merging

### The Iron Law of Systematic Debugging

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

### The Four Phases

**Phase 1: Root Cause Investigation**

1. **Read error messages carefully** — they often contain the exact solution
2. **Reproduce consistently** — exact steps, every time
3. **Check recent changes** — git diff, new dependencies, config changes
4. **Gather evidence in multi-component systems:**
   ```bash
   # Layer 1: Check environment propagation
   echo "=== Env vars: ===" && env | grep MY_VAR || echo "NOT SET"
   
   # Layer 2: Add diagnostic logging at each boundary
   console.log('[auth] Input:', { userId, scope })
   console.log('[auth] Token:', token ? 'SET' : 'UNSET')
   
   # Layer 3: Trace actual data flow
   console.log('[db] Query result:', JSON.stringify(result, null, 2))
   ```
5. **Trace data flow** — where does the bad value originate? Trace backward.

**Phase 2: Pattern Analysis**

- Find working examples of similar code in the codebase
- Compare working vs. broken code — list every difference
- Understand dependencies (config, environment, assumptions)

**Phase 3: Hypothesis and Testing**

- State your hypothesis: *"I think X is the root cause because Y"*
- Make the smallest possible change to test it
- One variable at a time — never multiple fixes at once
- If it didn't work, form a NEW hypothesis

**Phase 4: Implementation**

- Create a failing test case FIRST (use TDD section)
- Implement the single fix that addresses root cause
- Verify the fix (tests pass, issue resolved, no regressions)
- If 3+ fixes have failed: **question the architecture**, not the symptoms

### Debugging Red Flags — STOP and Return to Phase 1

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "It's probably X, let me fix that"
- "One more fix attempt" (after already trying 2+)
- Each fix reveals a new problem in a different place

**If 3+ fixes failed:** The architecture may be wrong. Discuss with your team before attempting more fixes.

### Quick Debugging Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| Root Cause | Read errors, reproduce, gather evidence | Understand WHAT and WHY |
| Pattern | Find working examples, compare | Identify differences |
| Hypothesis | Form theory, test minimally | Confirmed or new hypothesis |
| Implementation | Write test, fix, verify | Bug resolved, tests pass |

### Code Review Automation

```bash
# Analyze PR complexity and risk
python scripts/pr_analyzer.py /path/to/repo

# Compare specific branches
python scripts/pr_analyzer.py . --base main --head feature-branch

# Check code quality
python scripts/code_quality_checker.py /path/to/code

# Check specific language
python scripts/code_quality_checker.py . --language python

# Generate full review report
python scripts/review_report_generator.py /path/to/repo

# Markdown output
python scripts/review_report_generator.py . --format markdown --output review.md
```

**Review Verdicts:**
| Score | Verdict |
|-------|---------|
| 90+ with no high issues | Approve |
| 75+ with ≤2 high issues | Approve with suggestions |
| 50–74 | Request changes |
| < 50 or critical issues | Block |

### Code Quality Thresholds

| Issue | Threshold | Action |
|-------|-----------|--------|
| Long function | > 50 lines | Extract to smaller functions |
| Large file | > 500 lines | Split into modules |
| God class | > 20 methods | Apply Single Responsibility |
| Too many params | > 5 | Use options object or builder |
| Deep nesting | > 4 levels | Extract to functions, guard clauses |
| High complexity | > 10 branches | Extract to strategy pattern |

### Code Review Checklist

**Pre-review:**
- [ ] Build passes
- [ ] All tests pass
- [ ] PR description explains what and why
- [ ] No unrelated changes

**Correctness:**
- [ ] Logic handles edge cases
- [ ] Error handling is present and correct
- [ ] No data races or concurrency issues

**Security:**
- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user-controlled data
- [ ] No SQL injection vulnerabilities
- [ ] Authorization checks on all protected endpoints

**Performance:**
- [ ] No N+1 queries
- [ ] No unbounded collection operations
- [ ] Appropriate use of caching

**Maintainability:**
- [ ] Clear, descriptive variable and function names
- [ ] No magic numbers (use named constants)
- [ ] No TODO/FIXME without tracking issues
- [ ] No `any` types in TypeScript

**Testing:**
- [ ] New code has tests
- [ ] Tests cover error cases and edge cases
- [ ] No tests of implementation details

### Language-Specific Code Standards

**TypeScript:**
```typescript
// Type annotations on all public functions
function processUser(userId: string, options: ProcessOptions): Promise<User>

// Avoid `any` — use `unknown` + type guards
function parseJSON(input: unknown): Record<string, unknown> {
  if (typeof input !== 'string') throw new TypeError('Expected string');
  return JSON.parse(input);
}

// Prefer const assertions
const ROLES = ['admin', 'user', 'guest'] as const;
type Role = typeof ROLES[number];
```

**Python:**
```python
# Type hints on all functions
def process_user(user_id: str, *, dry_run: bool = False) -> User:
    ...

# Use dataclasses for data containers
from dataclasses import dataclass, field
@dataclass
class ProcessOptions:
    dry_run: bool = False
    timeout: float = 30.0

# Context managers for resources
with open(file_path) as f:
    content = f.read()
```

---

## Section 8: DevOps & CI/CD

### When to Use This Section
- Setting up CI/CD pipelines for a project
- Deploying applications to cloud infrastructure
- Containerizing applications with Docker/Kubernetes
- Managing infrastructure as code

### Pipeline Generation

```bash
# Generate GitHub Actions pipeline
python scripts/pipeline_generator.py ./my-project --platform github

# Generate CircleCI pipeline
python scripts/pipeline_generator.py ./my-project --platform circleci

# Analyze existing pipeline
python scripts/deployment_manager.py --analyze
```

### GitHub Actions Patterns

**Complete CI/CD Pipeline:**
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Security Scan
        run: python scripts/security_scanner.py . --severity high
      - name: Vulnerability Assessment
        run: python scripts/vulnerability_assessor.py . --severity critical

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    outputs:
      image-digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4
      - name: Login to Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build and Push
        id: build
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/app \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ needs.build.outputs.image-digest }}
          kubectl rollout status deployment/app
```

**Security Scan Gate:**
```yaml
# .github/workflows/security.yml
name: Security Scan
on:
  pull_request:
    branches: [main, develop]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Security Scanner
        run: python scripts/security_scanner.py . --severity high
      - name: Vulnerability Assessment
        run: python scripts/vulnerability_assessor.py . --severity critical
      - name: Compliance Check
        run: python scripts/compliance_checker.py . --framework soc2
```

### Infrastructure as Code (Terraform)

```bash
# Scaffold Terraform modules
python scripts/terraform_scaffolder.py ./infrastructure --cloud aws

# Analyze existing Terraform
python scripts/terraform_scaffolder.py ./infrastructure --verbose
```

**Terraform Module Structure:**
```
infrastructure/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── modules/
│   ├── vpc/
│   ├── eks/
│   └── rds/
└── environments/
    ├── staging/
    └── production/
```

**Example EKS Module:**
```hcl
# modules/eks/main.tf
resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks.arn
  version  = var.kubernetes_version

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.eks.id]
  }

  encryption_config {
    provider {
      key_arn = var.kms_key_arn
    }
    resources = ["secrets"]
  }

  depends_on = [aws_iam_role_policy_attachment.eks]
}
```

### Deployment Strategies

**Blue-Green Deployment:**
```bash
# Deploy to green environment
kubectl apply -f k8s/green/

# Run smoke tests
./scripts/smoke-test.sh https://green.example.com

# Switch traffic
kubectl patch service app -p '{"spec":{"selector":{"slot":"green"}}}'

# Keep blue for rollback
# kubectl patch service app -p '{"spec":{"selector":{"slot":"blue"}}}'
```

**Canary Deployment:**
```yaml
# k8s/canary.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"  # 10% to canary
spec:
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-canary
                port: { number: 80 }
```

**Rolling Update:**
```yaml
# k8s/deployment.yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Create 1 new pod before removing old
      maxUnavailable: 0  # Zero downtime
```

### Container Best Practices

```dockerfile
# Multi-stage build for Node.js
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine AS runner
WORKDIR /app
# Run as non-root
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs
COPY --from=builder /app/node_modules ./node_modules
COPY --chown=nextjs:nodejs . .
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

### Kubernetes Operations

```bash
# Apply manifests
kubectl apply -f k8s/

# Check rollout status
kubectl rollout status deployment/app

# Rollback if needed
kubectl rollout undo deployment/app

# View logs
kubectl logs -f deployment/app --tail=100

# Scale
kubectl scale deployment/app --replicas=5

# Resource usage
kubectl top pods
kubectl top nodes
```

### Monitoring & Alerting

**Health Check Endpoint:**
```typescript
// GET /health
app.get('/health', async (req, res) => {
  const checks = await Promise.allSettled([
    db.$queryRaw`SELECT 1`,
    redis.ping(),
  ]);

  const status = checks.every(c => c.status === 'fulfilled') ? 200 : 503;

  res.status(status).json({
    status: status === 200 ? 'healthy' : 'degraded',
    timestamp: new Date().toISOString(),
    checks: {
      database: checks[0].status,
      redis: checks[1].status,
    },
  });
});
```

**Structured Logging:**
```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  redact: ['req.headers.authorization', 'body.password'],
});

// Request logging
logger.info({ userId, action: 'createOrder', orderId }, 'Order created');

// Error logging
logger.error({ err, userId, path: req.path }, 'Request failed');
```

---

## Section 9: Security Engineering

### When to Use This Section
- Implementing security controls on a new project
- Conducting security audits or code reviews
- Responding to vulnerability reports
- Designing secure architectures

### Security Scanning Toolkit

```bash
# Scan source code for vulnerabilities
python scripts/security_scanner.py /path/to/project

# Filter by severity
python scripts/security_scanner.py /path/to/project --severity high

# JSON output for CI/CD
python scripts/security_scanner.py /path/to/project --json --output report.json

# Assess dependency CVEs
python scripts/vulnerability_assessor.py /path/to/project --severity high

# Check compliance
python scripts/compliance_checker.py /path/to/project --framework soc2
python scripts/compliance_checker.py /path/to/project --framework gdpr
python scripts/compliance_checker.py /path/to/project --framework pci-dss
python scripts/compliance_checker.py /path/to/project --framework hipaa
```

**Security Scanner Detects:**
- Hardcoded secrets (API keys, passwords, AWS credentials, private keys)
- SQL injection (string concatenation, f-strings in queries)
- XSS (innerHTML assignment, unsafe DOM manipulation)
- Command injection (shell=True, exec/eval with user input)
- Path traversal (file operations with user input)

### OWASP Top 10 Prevention

| Vulnerability | Prevention |
|--------------|------------|
| A01: Broken Access Control | RBAC, deny by default, validate permissions server-side |
| A02: Cryptographic Failures | TLS 1.3+, AES-256-GCM, secure key management |
| A03: Injection | Parameterized queries, input validation, escape output |
| A04: Insecure Design | Threat modeling, secure design patterns, defense in depth |
| A05: Security Misconfiguration | Hardening guides, remove defaults, disable unused features |
| A06: Vulnerable Components | Dependency scanning, automated updates, SBOM |
| A07: Authentication Failures | MFA, rate limiting, secure password storage |
| A08: Data Integrity Failures | Code signing, integrity checks, secure CI/CD |
| A09: Security Logging Failures | Comprehensive audit logs, SIEM integration |
| A10: SSRF | URL validation, allowlist destinations, network segmentation |

### Secure Coding Checklist

**Input Validation:**
- [ ] All user input validated server-side
- [ ] Allowlists over denylists
- [ ] Context-appropriate sanitization (HTML, SQL, shell)

**Authentication:**
- [ ] Passwords hashed with bcrypt/Argon2 (min rounds: 12)
- [ ] MFA for sensitive operations
- [ ] Strong password policy (min 12 chars, complexity)
- [ ] Short-lived access tokens (15 min), longer refresh tokens (7 days)

**Session Management:**
- [ ] Secure random session IDs
- [ ] HttpOnly, Secure, SameSite=Strict cookie flags
- [ ] Session timeout (15 min idle)
- [ ] Token rotation on privilege escalation

**Secrets Management:**
- [ ] Environment variables or dedicated secrets manager
- [ ] Never commit secrets to version control
- [ ] Rotate credentials on team member departure
- [ ] Use `.env.example` with placeholder values

**Error Handling:**
- [ ] Log errors with context (never log secrets)
- [ ] Return generic messages to users
- [ ] Never expose stack traces in production

### Threat Modeling (STRIDE)

**Workflow:**
1. Define system scope (assets, trust boundaries, data flows)
2. Create data flow diagram (DFD)
3. Apply STRIDE to each DFD element
4. Score risks with DREAD
5. Prioritize and define mitigations

**STRIDE Categories:**
| Category | Security Property | Mitigation Focus |
|----------|-------------------|------------------|
| Spoofing | Authentication | MFA, certificates, strong auth |
| Tampering | Integrity | Signing, checksums, validation |
| Repudiation | Non-repudiation | Audit logs, digital signatures |
| Information Disclosure | Confidentiality | Encryption, access controls |
| Denial of Service | Availability | Rate limiting, redundancy |
| Elevation of Privilege | Authorization | RBAC, least privilege |

**STRIDE per DFD Element:**
| Element | S | T | R | I | D | E |
|---------|---|---|---|---|---|---|
| External Entity | X | | X | | | |
| Process | X | X | X | X | X | X |
| Data Store | | X | X | X | X | |
| Data Flow | | X | | X | X | |

```bash
# Run STRIDE threat modeling
python scripts/threat_modeler.py --component "Authentication Service"

# Scan for hardcoded secrets
python scripts/secret_scanner.py /path/to/project
```

### Security Architecture: Defense in Depth

```
Layer 1: PERIMETER
  WAF, DDoS mitigation, DNS filtering, rate limiting

Layer 2: NETWORK
  Segmentation, IDS/IPS, network monitoring, VPN, mTLS

Layer 3: HOST
  Endpoint protection, OS hardening, patching, EDR

Layer 4: APPLICATION
  Input validation, authentication, secure coding, SAST

Layer 5: DATA
  Encryption at rest/transit, access controls, DLP, backup
```

**Zero Trust Principles:**
- Verify explicitly (authenticate/authorize every request)
- Least privilege access (just-in-time, just-enough access)
- Assume breach (segment, monitor, detect lateral movement)

### Authentication Pattern Selection

| Use Case | Recommended Pattern |
|----------|---------------------|
| Web application | OAuth 2.0 + PKCE with OIDC |
| API authentication | JWT (RS256) + short expiration + refresh tokens |
| Service-to-service | mTLS with certificate rotation |
| CLI/Automation | API keys with IP allowlisting |
| High security | FIDO2/WebAuthn hardware keys |

### Cryptographic Algorithm Selection

| Use Case | Algorithm | Key Size |
|----------|-----------|----------|
| Symmetric encryption | AES-256-GCM | 256 bits |
| Password hashing | Argon2id | Use defaults |
| Message authentication | HMAC-SHA256 | 256 bits |
| Digital signatures | Ed25519 | 256 bits |
| Key exchange | X25519 | 256 bits |
| TLS | TLS 1.3 | N/A |

**Code Patterns:**
```javascript
// Password hashing (bcrypt)
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash(password, 12);
const valid = await bcrypt.compare(password, hash);

// Random tokens (cryptographically secure)
import { randomBytes } from 'crypto';
const token = randomBytes(32).toString('hex');

// BAD: Math.random()
// GOOD: crypto.getRandomValues()
const array = new Uint32Array(10);
crypto.getRandomValues(array);
```

### Compliance Frameworks

**SOC 2 Type II Controls:**
| Control | Category | Description |
|---------|----------|-------------|
| CC1 | Control Environment | Security policies, org structure |
| CC3 | Risk Assessment | Vulnerability scanning, threat modeling |
| CC6 | Logical Access | Authentication, authorization, MFA |
| CC7 | System Operations | Monitoring, logging, incident response |
| CC8 | Change Management | CI/CD, code review, deployment controls |

**GDPR Requirements:**
| Article | Requirement |
|---------|-------------|
| Art 25 | Privacy by design, data minimization |
| Art 32 | Security measures, encryption, pseudonymization |
| Art 33 | Breach notification (72 hours) |
| Art 17 | Right to erasure (data deletion) |
| Art 20 | Data portability (export capability) |

### Security Incident Response

```
PHASE 1: DETECT & IDENTIFY (0–15 min)
- Alert received and acknowledged
- Initial severity assessment (SEV-1 to SEV-4)
- Incident commander assigned
- Communication channel established

PHASE 2: CONTAIN (15–60 min)
- Affected systems identified
- Network isolation if needed
- Credentials rotated if compromised
- Evidence preserved (logs, memory dumps)

PHASE 3: ERADICATE (1–4 hours)
- Root cause identified
- Malware/backdoors removed
- Vulnerabilities patched
- Systems hardened

PHASE 4: RECOVER (4–24 hours)
- Systems restored from clean backup
- Services brought back online
- Enhanced monitoring enabled

PHASE 5: POST-INCIDENT (24–72 hours)
- Timeline documented
- Root cause analysis complete
- Lessons learned documented
- Stakeholder report delivered
```

**Incident Severity Levels:**
| Level | Description | Response Time |
|-------|-------------|---------------|
| P1 – Critical | Active breach, data exfiltration | Immediate |
| P2 – High | Confirmed compromise, contained | 1 hour |
| P3 – Medium | Potential compromise, investigating | 4 hours |
| P4 – Low | Suspicious activity, low impact | 24 hours |

---

## Section 10: Data Engineering & Analysis

### When to Use This Section
- Profiling and exploring datasets for quality issues
- Writing SQL queries across multiple warehouse dialects
- Creating charts and visualizations
- Applying statistical methods to data
- Validating data pipelines and analysis methodology

### Dataset Profiling

```python
import pandas as pd
import numpy as np

def profile_dataset(df: pd.DataFrame) -> dict:
    """Profile a dataset for quality issues."""
    profile = {
        'shape': df.shape,
        'dtypes': df.dtypes.to_dict(),
        'null_counts': df.isnull().sum().to_dict(),
        'null_pct': (df.isnull().mean() * 100).round(2).to_dict(),
        'duplicates': df.duplicated().sum(),
    }

    # Numeric column stats
    numeric_cols = df.select_dtypes(include=np.number).columns
    profile['numeric_stats'] = df[numeric_cols].describe().to_dict()

    # Outlier detection (IQR method)
    outliers = {}
    for col in numeric_cols:
        Q1, Q3 = df[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        n_outliers = ((df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)).sum()
        if n_outliers > 0:
            outliers[col] = int(n_outliers)
    profile['outliers'] = outliers

    return profile
```

**Data Quality Checklist:**
- [ ] Row count matches expected volume
- [ ] No unexpected null values in required columns
- [ ] Primary key uniqueness validated
- [ ] Date ranges are within expected bounds
- [ ] Categorical values match known domain values
- [ ] Numeric values within business-valid ranges
- [ ] No duplicate records

### SQL Across Major Dialects

**PostgreSQL:**
```sql
-- Window functions
SELECT
  user_id,
  order_date,
  amount,
  SUM(amount) OVER (
    PARTITION BY user_id
    ORDER BY order_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date DESC) AS rn
FROM orders;

-- CTEs for readability
WITH monthly_revenue AS (
  SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(amount) AS revenue
  FROM orders
  WHERE status = 'completed'
  GROUP BY 1
),
growth AS (
  SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
    ROUND(
      100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
      / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 2
    ) AS growth_pct
  FROM monthly_revenue
)
SELECT * FROM growth ORDER BY month;
```

**Snowflake:**
```sql
-- Semi-structured data with VARIANT
SELECT
  user_id,
  event_data:event_type::STRING AS event_type,
  event_data:properties:page::STRING AS page,
  event_data:timestamp::TIMESTAMP AS ts
FROM events
WHERE event_data:event_type = 'page_view';

-- Clustering and partitioning
CREATE TABLE orders
  CLUSTER BY (DATE_TRUNC('month', order_date))
AS SELECT * FROM source_orders;
```

**BigQuery:**
```sql
-- Array aggregation
SELECT
  user_id,
  ARRAY_AGG(
    STRUCT(product_id, quantity, unit_price)
    ORDER BY created_at
  ) AS order_items
FROM order_items
GROUP BY user_id;

-- Approximate aggregations (fast on large tables)
SELECT
  country,
  APPROX_COUNT_DISTINCT(user_id) AS approx_users,
  APPROX_QUANTILES(revenue, 100)[OFFSET(50)] AS median_revenue
FROM sessions
GROUP BY country;
```

**Databricks / Spark SQL:**
```sql
-- Delta Lake time travel
SELECT * FROM orders VERSION AS OF 5;
SELECT * FROM orders TIMESTAMP AS OF '2026-01-01';

-- Optimize and Z-order
OPTIMIZE orders ZORDER BY (user_id, order_date);

-- Merge (upsert)
MERGE INTO orders AS target
USING updates AS source
ON target.order_id = source.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

**Query Optimization Patterns:**
```sql
-- Use EXISTS instead of IN for large subqueries
-- SLOW:
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 100);

-- FAST:
SELECT u.* FROM users u WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.amount > 100
);

-- Index-friendly date filtering
-- SLOW (function on indexed column):
WHERE YEAR(created_at) = 2026

-- FAST (range on indexed column):
WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'

-- Covering index for common queries
CREATE INDEX idx_orders_user_date_amount
ON orders(user_id, order_date)
INCLUDE (amount, status);
```

### Data Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Seaborn theme
sns.set_theme(style='whitegrid', palette='muted', font_scale=1.2)

# Distribution plot with annotations
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=df, x='revenue', bins=50, kde=True, ax=ax)
ax.set_title('Revenue Distribution', fontsize=14, fontweight='bold')
ax.set_xlabel('Revenue ($)')
ax.set_ylabel('Count')
plt.tight_layout()
plt.savefig('revenue_dist.png', dpi=150, bbox_inches='tight')

# Interactive Plotly chart
fig = px.scatter(
    df,
    x='customer_age',
    y='lifetime_value',
    color='segment',
    size='order_count',
    hover_data=['customer_id'],
    title='Customer Lifetime Value by Segment',
    labels={'customer_age': 'Age', 'lifetime_value': 'LTV ($)'},
)
fig.update_layout(template='plotly_white')
fig.write_html('ltv_scatter.html')
```

**Chart Type Selection Guide:**
| Data Type | Comparison | Use Chart |
|-----------|-----------|-----------|
| Numeric over time | Trend | Line chart |
| Numeric categories | Ranking | Bar chart (horizontal for long labels) |
| Part-to-whole | Composition | Stacked bar, treemap |
| Two numeric vars | Correlation | Scatter plot |
| Distribution | Shape | Histogram, violin, box plot |
| Geographic | Spatial | Choropleth, bubble map |
| Proportions (≤5 parts) | Composition | Pie/donut (use sparingly) |

**Accessibility in Charts:**
```python
# Use colorblind-safe palettes
PALETTE = ['#0072B2', '#E69F00', '#009E73', '#CC79A7', '#56B4E9']

# Add pattern fill for black-and-white printing
ax.bar(x, height, hatch='///', color=PALETTE[0])

# Always include alt text metadata
fig.update_layout(
    title=dict(text='<b>Revenue by Quarter</b>'),
    annotations=[dict(
        text='<i>Accessible description: Bar chart showing Q1-Q4 revenue...</i>',
        visible=False,  # For screen readers via aria
    )],
)
```

### Statistical Analysis

```python
from scipy import stats
import numpy as np

# Descriptive statistics
def describe_column(series: pd.Series) -> dict:
    return {
        'n': len(series.dropna()),
        'mean': series.mean(),
        'median': series.median(),
        'std': series.std(),
        'skewness': series.skew(),
        'kurtosis': series.kurtosis(),
        'q1': series.quantile(0.25),
        'q3': series.quantile(0.75),
        'iqr': series.quantile(0.75) - series.quantile(0.25),
    }

# Hypothesis testing — t-test
def ab_test(control: np.ndarray, treatment: np.ndarray, alpha: float = 0.05) -> dict:
    t_stat, p_value = stats.ttest_ind(control, treatment)
    effect_size = (treatment.mean() - control.mean()) / np.sqrt(
        ((len(control) - 1) * control.std()**2 + (len(treatment) - 1) * treatment.std()**2)
        / (len(control) + len(treatment) - 2)
    )
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'significant': p_value < alpha,
        'cohens_d': effect_size,
        'control_mean': control.mean(),
        'treatment_mean': treatment.mean(),
        'lift_pct': 100 * (treatment.mean() - control.mean()) / control.mean(),
    }

# Outlier detection — Z-score method
def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    z_scores = np.abs(stats.zscore(series.dropna()))
    return series[z_scores > threshold]

# Correlation matrix
def correlation_analysis(df: pd.DataFrame, method: str = 'spearman') -> pd.DataFrame:
    corr = df.select_dtypes(include=np.number).corr(method=method)
    return corr
```

### Data Validation Methodology

```python
import great_expectations as gx

# Define expectations
context = gx.get_context()
suite = context.add_expectation_suite('orders.critical')

# Validate
validator = context.get_validator(
    datasource_name='my_db',
    data_asset_name='orders',
    expectation_suite=suite,
)

# Required validations for any dataset
validator.expect_column_to_exist('order_id')
validator.expect_column_values_to_not_be_null('order_id')
validator.expect_column_values_to_be_unique('order_id')
validator.expect_column_values_to_be_between('amount', 0, 100_000)
validator.expect_column_values_to_be_in_set('status', ['pending', 'completed', 'cancelled'])
validator.expect_column_values_to_match_regex('email', r'^[^@]+@[^@]+\.[^@]+$')

results = validator.validate()
assert results.success, f"Validation failed: {results}"
```

**Data Validation Checklist:**
- [ ] Schema matches expected structure (column names, types)
- [ ] No nulls in required columns
- [ ] Primary key uniqueness
- [ ] Foreign key referential integrity
- [ ] Business rules (positive amounts, valid statuses)
- [ ] Row count within expected range
- [ ] No duplicate records
- [ ] Temporal consistency (end_date > start_date)
- [ ] Survivorship bias check (are you missing inactive records?)

---

## Section 11: Changelog & Documentation

### When to Use This Section
- Preparing release notes for a new version
- Creating weekly product update summaries
- Generating README or API documentation

### Changelog Generation from Git

**Basic usage:**
```
Create a changelog from commits since last release
Generate changelog for all commits from the past week
Create release notes for version 2.5.0
Create a changelog for commits between March 1 and March 15
```

**With custom guidelines:**
```
Create a changelog for commits since v2.4.0, using my changelog
guidelines from CHANGELOG_STYLE.md
```

**Workflow:**
1. Check dependency files for exact versions (`package.json`, `requirements.txt`)
2. Look up library changelogs for any upgrades mentioned
3. Translate technical commits into user-facing language
4. Filter out internal commits (refactoring, CI, tests)
5. Group by category: Features, Improvements, Fixes, Security

**Output Format:**
```markdown
# Updates — Week of March 3, 2026

## New Features

- **Team Workspaces**: Create separate workspaces for different projects.
  Invite team members and keep everything organized.

- **Keyboard Shortcuts**: Press ? to see all available shortcuts.
  Navigate faster without touching your mouse.

## Improvements

- **Faster Sync**: Files now sync 2x faster across devices
- **Better Search**: Search now includes file contents, not just titles

## Bug Fixes

- Fixed issue where large images would not upload
- Resolved timezone confusion in scheduled posts
- Corrected notification badge count

## Security

- Updated dependency to resolve CVE-2026-1234 (high severity)
```

**Commit Categories:**
| Conventional Commit Prefix | Changelog Section |
|---------------------------|-------------------|
| `feat:`, `feature:` | New Features |
| `perf:`, `improve:` | Improvements |
| `fix:`, `bugfix:` | Bug Fixes |
| `security:`, `vuln:` | Security |
| `break:`, `BREAKING:` | Breaking Changes |
| `refactor:`, `test:`, `ci:` | (filtered out) |

### README Generation

**Essential README Sections:**
```markdown
# Project Name

One-line description of what this does.

## Quick Start

```bash
npm install
cp .env.example .env
npm run dev
```

## Features

- Feature 1 with brief description
- Feature 2 with brief description

## Architecture

Brief description + link to architecture docs

## Development

Prerequisites, setup instructions, commands

## Testing

How to run tests, coverage requirements

## Deployment

How to deploy to production

## Contributing

Branch conventions, PR process, code standards

## License

MIT / Apache 2.0 / etc.
```

### API Documentation

```typescript
/**
 * @openapi
 * /users/{id}:
 *   get:
 *     summary: Get user by ID
 *     tags: [Users]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: The user's unique identifier
 *     responses:
 *       200:
 *         description: User found
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/User'
 *       404:
 *         description: User not found
 *       401:
 *         description: Authentication required
 */
app.get('/users/:id', authenticate, async (req, res) => {
  // ...
});
```

**Documentation Best Practices:**
- [ ] Every public function/method has a docstring
- [ ] All parameters documented with types and constraints
- [ ] Return values and error cases described
- [ ] Code examples provided for complex functions
- [ ] CHANGELOG.md updated with every release
- [ ] `CONTRIBUTING.md` describes development workflow
- [ ] Architecture Decision Records (ADRs) in `docs/adr/`
- [ ] Runbooks for operations tasks in `docs/runbooks/`

---

## Section 12: Unique Perplexity Computer Capabilities

These capabilities are exclusive to Perplexity Computer and complement the engineering workflows above.

### Live Web Research for Engineering Decisions

When evaluating libraries, frameworks, or packages, Perplexity Computer can fetch real-time information that goes beyond any training cutoff:

**Use cases:**
- "What's the latest stable version of Next.js and what changed?"
- "Are there known security issues with lodash 4.17.20?"
- "How does Bun compare to Node.js for our API use case in 2026?"
- "What does the official Prisma documentation say about connection pooling with serverless functions?"
- "Look up the breaking changes in React 19 before I upgrade"

This fills the gap where Claude Code skills have training cutoff dates — Perplexity can verify package docs, changelogs, CVEs, and Stack Overflow answers in real time.

### Website Deployment in Minutes

Perplexity Computer can build and deploy complete websites without a separate infrastructure setup:

**Workflow:**
1. Describe your website requirements
2. Perplexity generates the complete site (HTML/CSS/JS or React)
3. The site is deployed and accessible at a shareable URL
4. Iterate on design with AI-assisted updates

**Best for:**
- Landing pages, documentation sites, marketing microsites
- Prototype/MVP deployments for user testing
- Static sites from markdown content
- Internal tools and dashboards

### AI Image Generation for UI Mockups

Generate visual assets directly in your engineering workflow:

**Use cases:**
- "Generate a hero banner for the product landing page"
- "Create a placeholder image for user avatars (512x512, professional headshot style)"
- "Design an icon for the notifications feature"
- "Generate a mockup of what the dashboard could look like before I code it"

**Supported aspect ratios:** 1:1, 16:9, 9:16, 4:3, 3:4

### 400+ App Integrations

Perplexity Computer integrates with external services your engineering workflow already uses:

| Category | Examples |
|----------|---------|
| Version Control | GitHub, GitLab, Bitbucket |
| Project Management | Jira, Linear, Asana, Trello |
| Communication | Slack, Microsoft Teams |
| Cloud Platforms | AWS, GCP, Azure |
| Databases | Supabase, PlanetScale, Neon |
| Monitoring | Datadog, PagerDuty, Grafana |
| CI/CD | GitHub Actions, CircleCI, Vercel |
| Analytics | Mixpanel, Amplitude, PostHog |

### Scheduled Monitoring for Deployments

Set up automated checks that run on a schedule:

**Examples:**
- Monitor a URL for uptime every 5 minutes
- Check that a deployment succeeded after a CI run
- Alert if API response time exceeds 500ms
- Verify database backup completed successfully

### Real-Time Package & Library Information

Unlike static training data, Perplexity can look up:
- Latest package versions on npm, PyPI, crates.io
- Known CVEs and security advisories
- Migration guides between major versions
- Community-reported issues and workarounds
- Benchmark comparisons published after training cutoff

### Technology Comparison Research

For architecture decisions, Perplexity can synthesize current community knowledge:

**Examples:**
- "Compare Prisma vs Drizzle for our Next.js + PostgreSQL stack as of 2026"
- "What are developers saying about switching from REST to tRPC?"
- "Is Redis still the recommended choice for rate limiting, or are there better alternatives?"
- "What are the current production adoption rates of Bun vs Node.js?"

---

## Quick Reference: When to Use Which Skill Section

| Task | Section | Key Commands/Patterns |
|------|---------|----------------------|
| Design a new system | §2 Architecture | `project_architect.py`, ADR template |
| Build a React component | §3 Frontend | `component_generator.py`, patterns |
| Design a REST API | §4 Backend | `api_scaffolder.py`, OpenAPI |
| Start a new full-stack project | §5 Fullstack | `project_scaffolder.py` |
| Write tests for existing code | §6 Testing | `test_suite_generator.py`, TDD cycle |
| Debug a failing test/bug | §7 Debugging | Four-phase root cause analysis |
| Review a pull request | §7 Code Review | `pr_analyzer.py`, checklist |
| Set up CI/CD | §8 DevOps | GitHub Actions templates |
| Security audit | §9 Security | `security_scanner.py`, OWASP checklist |
| Write complex SQL | §10 Data | Dialect-specific patterns |
| Visualize data | §10 Data | Chart type selection guide |
| Write release notes | §11 Changelog | Git-to-changelog workflow |
| Lookup current library docs | §12 Perplexity | Live web research |
| Deploy a website | §12 Perplexity | Perplexity deployment |

---

## Skill Combination Workflows

### Workflow A: Start a New SaaS Product

1. **§2 Architecture** — Create system diagram + ADR for key decisions
2. **§5 Fullstack** — Scaffold project with `project_scaffolder.py nextjs my-saas`
3. **§8 DevOps** — Generate CI/CD pipeline with security gates
4. **§9 Security** — Run initial security scan, set up compliance baseline
5. **§6 Testing** — Set up Jest + Playwright, establish 80% coverage target
6. **§12 Perplexity** — Research current library versions and deploy preview

### Workflow B: Fix a Bug in Production

1. **§7 Debugging** — Phase 1 root cause investigation (read errors, reproduce)
2. **§6 Testing** — Write a failing test that reproduces the bug
3. **§7 Debugging** — Implement single fix, verify tests pass
4. **§8 DevOps** — Deploy via CI/CD pipeline, monitor

### Workflow C: Security Audit Before Launch

1. **§9 Security** — `security_scanner.py` + `vulnerability_assessor.py`
2. **§9 Security** — `compliance_checker.py --framework soc2`
3. **§9 Security** — STRIDE threat model for critical components
4. **§7 Code Review** — `review_report_generator.py` for all new code
5. **§12 Perplexity** — Research any CVEs in dependencies that emerged post-training

### Workflow D: Data Analysis Pipeline

1. **§10 Data** — Profile dataset for quality issues
2. **§10 Data** — Write SQL queries (dialect-appropriate)
3. **§10 Data** — Validate data with Great Expectations
4. **§10 Data** — Visualize results with appropriate chart types
5. **§6 Testing** — Write tests for data transformation logic
6. **§11 Docs** — Document analysis methodology and findings
