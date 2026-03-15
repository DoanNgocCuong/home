<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# 1. Mỗi pod là mấy worker?

Không có “quy tắc” cố định là mỗi pod phải chạy bao nhiêu worker; số worker per pod là do mình thiết kế dựa trên app + resource limit của pod.[^1][^2]

## Ý chính

- Về Kubernetes:
    - Pod chỉ là “logical host” chứa 1 hoặc nhiều container, share cùng tài nguyên (CPU/RAM, network, volume) trên một worker node.[^3][^2]
    - Kubernetes không định nghĩa khái niệm “worker” bên trong pod; “worker” thường là process/app level (ví dụ worker của Gunicorn, Celery…).[^4][^2]
- Về thực tế cấu hình worker per pod (ví dụ web bằng Gunicorn):
    - Doc Gunicorn hay gợi ý công thức $(2 \times \text{num\_cores}) + 1$ cho VM/bare metal, nhưng khi lên container, best practice thường là 1–2 worker mỗi container (tức mỗi pod) để dễ scale ngang và tránh tranh chấp tài nguyên.[^1]
    - Nếu tăng số worker trong 1 pod thì nên tăng resource (CPU/memory requests/limits) tương ứng, nếu không dễ timeout/throttling do các worker tranh CPU.[^1]


## Gợi ý cho case của bạn

- Nếu pod chỉ chạy 1 container web (Gunicorn/Uvicorn workers, v.v.):
    - Start: 1–2 worker per pod, rồi scale pod replica lên nhiều bản để chịu tải.[^1]
    - Giữ mỗi pod “nhỏ, đồng nhất” để autoscaler hoạt động hiệu quả và việc deploy/rollback đơn giản.
- Nếu bạn đang nói tới worker job/queue (Celery/RQ/…):
    - Xem mỗi worker có cần nhiều CPU không; job nặng CPU thì 1 worker/pod hoặc 2 worker/pod là hợp lý.[^4]
    - Job nhẹ/IO-bound (đợi network/db nhiều) có thể tăng hơn, nhưng vẫn nên ưu tiên scale bằng số pod.

Nếu bạn gửi thêm: loại app (web/worker), dùng gì (Gunicorn, Celery, …) và resource mỗi pod (CPU/RAM requests/limits) thì có thể thiết kế luôn con số worker cụ thể cho từng pod.
<span style="display:none">[^10][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://blog.graywind.org/posts/gunicorn-in-containers/

[^2]: https://kubernetes.io/docs/concepts/workloads/pods/

[^3]: https://viblo.asia/p/kubernetes-series-bai-2-kubernetes-pod-thanh-phan-de-chay-container-YWOZr3QElQ0

[^4]: https://dzone.com/articles/kubernetes-work-queue-parallel-processing

[^5]: https://kubernetes.io/vi/docs/tutorials/kubernetes-basics/explore/explore-intro/

[^6]: https://www.reddit.com/r/kubernetes/comments/1gaey29/queueing_pods_on_kubernetes/

[^7]: https://translate.google.com/translate?u=https%3A%2F%2Fwww.cloudzero.com%2Fblog%2Fkubernetes-node-vs-pod%2F\&hl=vi\&sl=en\&tl=vi\&client=srp

[^8]: https://viettelidc.com.vn/tin-tuc/kubernetes-pod-la-gi

[^9]: https://translate.google.com/translate?u=https%3A%2F%2Fsematext.com%2Fglossary%2Fkubernetes-pod%2F\&hl=vi\&sl=en\&tl=vi\&client=srp

[^10]: https://learnkube.com/kubernetes-node-size

