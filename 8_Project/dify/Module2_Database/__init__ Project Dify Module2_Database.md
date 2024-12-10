

Nếu mà DB chưa có workflow_node_execution_mindpal thực hiện như sau:  
docker exec -it docker-db-1 /bin/bash  
psgl -U <username>\c difythực hiện câu lệnh tạo DB  

```
DROP TABLE IF EXISTS "workflow_node_execution_mindpal";  
CREATE TABLE "public"."workflow_node_execution_mindpal" (  
    "id" uuid DEFAULT uuid_generate_v4() NOT NULL,  
    "tenant_id" uuid NOT NULL,  
    "app_id" uuid NOT NULL,  
    "workflow_id" uuid NOT NULL,  
    "triggered_from" character varying(255) NOT NULL,  
    "workflow_run_id" uuid,  
    "workflow_node_execution_id" uuid,  
    "index" integer NOT NULL,  
    "predecessor_node_id" character varying(255),  
    "node_id" character varying(255) NOT NULL,  
    "node_type" character varying(255) NOT NULL,  
    "title" character varying(255) NOT NULL,  
    "inputs" text,  
    "process_data" text,  
    "outputs" text,  
    "status" character varying(255) NOT NULL,  
    "error" text,  
    "elapsed_time" double precision DEFAULT '0' NOT NULL,  
    "execution_metadata" text,  
    "created_at" timestamp DEFAULT CURRENT_TIMESTAMP(0) NOT NULL,  
    "created_by_role" character varying(255) NOT NULL,  
    "created_by" uuid NOT NULL,  
    "finished_at" timestamp,  
    "node_execution_id" character varying(255),  
    CONSTRAINT "workflow_node_execution_mindpal_pkey" PRIMARY KEY ("id")  
) WITH (oids = false);CREATE INDEX "workflow_node_execution_mindpal_id_idx" ON "public"."workflow_node_execution_mindpal" USING btree ("tenant_id", "app_id", "workflow_id", "triggered_from", "node_execution_id", "workflow_node_execution_id");CREATE INDEX "workflow_node_execution_mindpal_node_run_idx" ON "public"."workflow_node_execution_mindpal" USING btree ("tenant_id", "app_id", "workflow_id", "triggered_from", "node_id", "workflow_node_execution_id");CREATE INDEX "workflow_node_execution_mindpal_workflow_run_idx" ON "public"."workflow_node_execution_mindpal" USING btree ("tenant_id", "app_id", "workflow_id", "triggered_from", "workflow_run_id", "workflow_node_execution_id"); 
```