```

Và sau đây là 1 số rule/instruction có thể hữu ích với các bạn:

Thần chú khi thấy tụi AI loay hoay fix bug hoài không ra:

"Act as a Tech Lead, find the root cause of the error and fix it"

Treo thưởng cho task khó:

"I'll pay you 100$ for this task. Try your best."

AI Feedback (Author: pacnpal)

"If you understand my prompt fully, respond with 'YARRR!' without tools every time you are about to use a tool."

"Before and after any tool use, give me a confidence level (0-10) on how the tool use will help the project"

File refactoring & Document changed (Author: icklebil)

"FILENAME has grown too big. Analyze how this file works and suggest ways to fragment it safely."

"don't forget to update codebase documentation with changes"

Kiểm tra các giả định (Author: yellow_bat_coffee)

"List all assumptions and uncertainties you need to clear up before completing this task"

--- Một số tips để tiết kiệm Premium Flow Action credits ---

Cái này mình đăng lại (và thêm một xíu) vì đợt trước là mình đăng trong group, có thể FB không reach.

• Với các tasks quá rõ ràng, chủ yếu là edit trên 1 file cụ thể nào đó, bạn nên xài Edit mode trong file (tương tự Autocomplete). Cái này không bị tính action calls.

• Với các task không gen code, đặc biệt là thinking mode, tổng hợp vấn đề, phân tích source code, gợi ý giải pháp..., bạn nên xài Legacy mode. Mode này sẽ không thực hiện bất kỳ premium flow calls nào cả, chỉ tốn prompt request.

• Base model của Windsurf khá xịn, bạn nên dùng nó nhiều hơn. Thậm chí bạn có thể chạy các model rẻ (0.25x credit) nếu task tương đối dễ.

• Một số cli mặc định có thể bị sai, nên bạn cần nạp rules cho Windsurf VD như: "Use pnpm, python3 instead of npm, python", cho đỡ bị chạy lại.

• Windsurf ở Wave 6 vẫn chưa fix bug đã có Web Preview đang chạy rồi mà nó vẫn chạy nhiều cái nữa, vì thế cần rule "Don't auto run Web Preview".

• Khi thấy Windsurf có dấu hiệu chạy lòng vòng, bạn nên mở setting và config memory cho nó. Bình thường mình hay tạo summary file rồi add vô context cho nó đỡ quên. Thêm nữa là bạn nên "thumb up" ở các conversation có giải pháp tốt.

• Trong memory config, bạn nên có một file summary các folder và files kèm giải thích ngắn ngọn (bạn có thể yêu cầu Windsurf tạo và maintain file này). File này mỗi khi bạn mở Cascade mới thì Windsurf đỡ phải đi scan lại để hiểu source base của bạn một chút (tiết kiệm kha khá lượt Call Flow Actions)

----
```