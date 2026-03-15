
```bash
Huy Trần Quốc WECOMMIT, [10/23/2025 12:28 PM]
{
  explainVersion: '1',
  queryPlanner: {
    namespace: 'Wecommit.orders',
    parsedQuery: {
      '$and': [
        {
          status: {
            '$eq': 'paid'
          }
        },
        {
          amount: {
            '$gt': 100
          }
        }
      ]
    },
    indexFilterSet: false,
    queryHash: '609FE0DA',
    planCacheShapeHash: '609FE0DA',
    planCacheKey: '7F25CF6F',
    optimizationTimeMillis: 0,
    maxIndexedOrSolutionsReached: false,
    maxIndexedAndSolutionsReached: false,
    maxScansToExplodeReached: false,
    prunedSimilarIndexes: false,
    winningPlan: {
      isCached: false,
      stage: 'FETCH',
      filter: {
        amount: {
          '$gt': 100
        }
      },
      inputStage: {
        stage: 'IXSCAN',
        keyPattern: {
          status: 1
        },
        indexName: 'status_1',
        isMultiKey: false,
        multiKeyPaths: {
          status: []
        },
        isUnique: false,
        isSparse: false,
        isPartial: false,
        indexVersion: 2,
        direction: 'forward',
        indexBounds: {
          status: [
            '["paid", "paid"]'
          ]
        }
      }
    },
    rejectedPlans: [
      {
        isCached: false,
        stage: 'FETCH',
        filter: {
          amount: {
            '$gt': 100
          }
        },
        inputStage: {
          stage: 'IXSCAN',
          keyPattern: {
            status: 1,
            customer_id: 1
          },
          indexName: 'status_1_customer_id_1',
          isMultiKey: false,
          multiKeyPaths: {
            status: [],
            customer_id: []
          },
          isUnique: false,
          isSparse: false,
          isPartial: false,
          indexVersion: 2,
          direction: 'forward',
          indexBounds: {
            status: [
              '["paid", "paid"]'
            ],
            customer_id: [
              '[MinKey, MaxKey]'
            ]
          }
        }
      },
      {
        isCached: false,
        stage: 'FETCH',
        filter: {
          status: {
            '$eq': 'paid'
          }
        },
        inputStage: {
          stage: 'IXSCAN',
          keyPattern: {
            amount: 1
          },
          indexName: 'amount_1',
          isMultiKey: false,
          multiKeyPaths: {
            amount: []
          },
          isUnique: false,
          isSparse: false,
          isPartial: false,
          indexVersion: 2,
          direction: 'forward',
          indexBounds: {
            amount: [
              '(100, inf]'
            ]
          }
        }
      }
    ]
  },
  executionStats: {
    executionSuccess: true,
    nReturned: 2,
    executionTimeMillis: 0,
    totalKeysExamined: 3,
    totalDocsExamined: 3,
    executionStages: {
      isCached: false,
      stage: 'FETCH',
      filter: {
        amount: {
          '$gt': 100
        }
      },
      nReturned: 2,
      executionTimeMillisEstimate: 0,
      works: 5,
      advanced: 2,
      needTime: 1,
      needYield: 0,
      saveState: 0,
      restoreState: 0,
      isEOF: 1,
      docsExamined: 3,
      alreadyHasObj: 0,
      inputStage: {
        stage: 'IXSCAN',
        nReturned: 3,
        executionTimeMillisEstimate: 0,
        works: 4,
        advanced: 3,
        needTime: 0,
        needYield: 0,
        saveState: 0,
        restoreState: 0,
        isEOF: 1,
        keyPattern: {
          status: 1
        },
        indexName: 'status_1',
        isMultiKey: false,
        multiKeyPaths: {
          status: []
        },
        isUnique: false,
        isSparse: false,
        isPartial: false,
        indexVersion: 2,
        direction: 'forward',
        indexBounds: {
          status: [
            '["paid", "paid"]'
          ]
        },
        keysExamined: 3,
        seeks: 1,
        dupsTested: 0,
        dupsDropped: 0
      }
    },
    allPlansExecution: [
      {
        nReturned: 2,
        executionTimeMillisEstimate: 0,
        totalKeysExamined: 3,
        totalDocsExamined: 3,
        score: 2.5002,

Huy Trần Quốc WECOMMIT, [10/23/2025 12:28 PM]
executionStages: {
          isCached: false,
          stage: 'FETCH',
          filter: {
            amount: {
              '$gt': 100
            }
          },
          nReturned: 2,
          executionTimeMillisEstimate: 0,
          works: 4,
          advanced: 2,
          needTime: 1,
          needYield: 0,
          saveState: 0,
          restoreState: 0,
          isEOF: 1,
          docsExamined: 3,
          alreadyHasObj: 0,
          inputStage: {
            stage: 'IXSCAN',
            nReturned: 3,
            executionTimeMillisEstimate: 0,
            works: 4,
            advanced: 3,
            needTime: 0,
            needYield: 0,
            saveState: 0,
            restoreState: 0,
            isEOF: 1,
            keyPattern: {
              status: 1
            },
            indexName: 'status_1',
            isMultiKey: false,
            multiKeyPaths: {
              status: []
            },
            isUnique: false,
            isSparse: false,
            isPartial: false,
            indexVersion: 2,
            direction: 'forward',
            indexBounds: {
              status: [
                '["paid", "paid"]'
              ]
            },
            keysExamined: 3,
            seeks: 1,
            dupsTested: 0,
            dupsDropped: 0
          }
        }
      },
      {
        nReturned: 2,
        executionTimeMillisEstimate: 0,
        totalKeysExamined: 3,
        totalDocsExamined: 3,
        score: 2.5002,
        executionStages: {
          isCached: false,
          stage: 'FETCH',
          filter: {
            amount: {
              '$gt': 100
            }
          },
          nReturned: 2,
          executionTimeMillisEstimate: 0,
          works: 4,
          advanced: 2,
          needTime: 1,
          needYield: 0,
          saveState: 1,
          restoreState: 0,
          isEOF: 1,
          docsExamined: 3,
          alreadyHasObj: 0,
          inputStage: {
            stage: 'IXSCAN',
            nReturned: 3,
            executionTimeMillisEstimate: 0,
            works: 4,
            advanced: 3,
            needTime: 0,
            needYield: 0,
            saveState: 1,
            restoreState: 0,
            isEOF: 1,
            keyPattern: {
              status: 1,
              customer_id: 1
            },
            indexName: 'status_1_customer_id_1',
            isMultiKey: false,
            multiKeyPaths: {
              status: [],
              customer_id: []
            },
            isUnique: false,
            isSparse: false,
            isPartial: false,
            indexVersion: 2,
            direction: 'forward',
            indexBounds: {
              status: [
                '["paid", "paid"]'
              ],
              customer_id: [
                '[MinKey, MaxKey]'
              ]
            },
            keysExamined: 3,
            seeks: 1,
            dupsTested: 0,
            dupsDropped: 0
          }
        }
      },
      {
        nReturned: 2,
        executionTimeMillisEstimate: 0,
        totalKeysExamined: 3,
        totalDocsExamined: 3,
        score: 2.5002,
        executionStages: {
          isCached: false,
          stage: 'FETCH',
          filter: {
            status: {
              '$eq': 'paid'
            }
          },
          nReturned: 2,
          executionTimeMillisEstimate: 0,
          works: 4,
          advanced: 2,
          needTime: 1,
          needYield: 0,
          saveState: 1,
          restoreState: 0,
          isEOF: 1,
          docsExamined: 3,
          alreadyHasObj: 0,
          inputStage: {
            stage: 'IXSCAN',
            nReturned: 3,
            executionTimeMillisEstimate: 0,
            works: 4,
            advanced: 3,
            needTime: 0,
            needYield: 0,
            saveState: 1,
            restoreState: 0,
            isEOF: 1,
            keyPattern: {
              amount: 1
            },
            indexName: 'amount_1',
            isMultiKey: false,
            multiKeyPaths: {

Huy Trần Quốc WECOMMIT, [10/23/2025 12:28 PM]
amount: []
            },
            isUnique: false,
            isSparse: false,
            isPartial: false,
            indexVersion: 2,
            direction: 'forward',
            indexBounds: {
              amount: [
                '(100, inf]'
              ]
            },
            keysExamined: 3,
            seeks: 1,
            dupsTested: 0,
            dupsDropped: 0
          }
        }
      }
    ]
  },
  queryShapeHash: '12CDE1B416BE2ED94B05DC56D81BB2EA2EA3373FE08DE8E6BE5A10C2837C4A15',
  command: {
    find: 'orders',
    filter: {
      status: 'paid',
      amount: {
        '$gt': 100
      }
    },
    '$db': 'Wecommit'
  },
  serverInfo: {
    host: 'DESKTOP-U747V0Q',
    port: 27017,
    version: '8.2.1',
    gitVersion: '3312bdcf28aa65f5930005e21c2cb130f648b8c3'
  },
  serverParameters: {
    internalQueryFacetBufferSizeBytes: 104857600,
    internalQueryFacetMaxOutputDocSizeBytes: 104857600,
    internalLookupStageIntermediateDocumentMaxSizeBytes: 104857600,
    internalDocumentSourceGroupMaxMemoryBytes: 104857600,
    internalQueryMaxBlockingSortMemoryUsageBytes: 104857600,
    internalQueryProhibitBlockingMergeOnMongoS: 0,
    internalQueryMaxAddToSetBytes: 104857600,
    internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600,
    internalQueryFrameworkControl: 'trySbeRestricted',
    internalQueryPlannerIgnoreIndexWithCollationForRegex: 1
  },
  ok: 1
}
```

---

Ông này ko có thói quen chọn Collection scan

Winning plan, tức là cho chạy thửu 100 thằng chọn giải thuật ngon nhất để chạy 
Và nó lưu winning plan này lại 

![](image/Pasted%20image%2020251023124246.png)

Điều chỉnh chiến lược thực thi ở: Query Setting 

