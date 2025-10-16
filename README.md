2311029  
Phan Vĩnh Nghiêm  
Môn học: Trí tuệ Nhân tạo  
Lớp: Sáng thứ 2 - thứ 6, tiết 1 - 4  
# Bài toán 8 quân xe
## Minh họa các thuật toán tìm kiếm để tìm ra lời giải với Goal được đặt bằng tay trước
![Giao diện][(Image_Readme/UI.png)](https://github.com/ngiempv/AI_CaNhan/blob/main/Image_Readme/UI.png)
# Chương trình bao gồm các tính năng:
  Tương tắc với giao diện:   
  Tự thiết lập trạng thái đích cho bài toán N-Xe trên một bàn cờ trực quan.  
  So sánh Song song: Theo dõi thuật toán hoạt động trên bàn cờ bên trái để khớp với trạng thái đích ở bàn cờ bên phải.  
  Hoạt ảnh Từng bước (Step-by-Step): Trực quan hóa rõ ràng quá trình khám phá, quay lui và ra quyết định của mỗi thuật toán.  
# Hướng dẫn sử dụng
  1. Chạy file python
  2. Thiết lập goal lên bàn cờ bên phải
  3. Chọn thuật toán
  4. start để bắt đầu mô phỏng
  5. Điều khiển Mô phỏng: Sử dụng các nút "Stop", "Reset", và "Restart" để điều khiển quá trình trực quan hóa.
# Các thuật toán tìm kiếm mù được triển khai:
  ## BFS (Breadth-First Search): 
  Duyệt qua tất cả các cột khả thi theo từng hàng, đảm bảo tìm ra giải pháp.
  ![BFS](https://github.com/user-attachments/assets/8348cc95-4b7f-478a-8b96-a0823f21874b)
  ## DFS: 
  Cho duyệt tương tự để có thể so sánh với BFS
  ![DFS](https://github.com/user-attachments/assets/915fd479-884a-4504-8018-1f6b21f37489)
  ## DLS (Depth-Limited Search): 
  Một biến thể của DFS, dừng tìm kiếm sau khi đạt đến một giới hạn độ sâu được xác định trước.
  ## IDS (Iterative Deepening Search): 
  Kết hợp lợi ích của BFS và DFS bằng cách thực hiện một loạt các tìm kiếm DLS với độ sâu tăng dần.
  ## UCS (Uniform-Cost Search): 
  Tìm đường đi có tổng chi phí thấp nhất. Trong mô hình này, nó hoạt động tương tự BFS vì chi phí mỗi bước là như nhau.
# Tìm kiếm có thông tin:
  ## A* Search: 
      Thuật toán A* là một thuật toán tìm kiếm có thông tin (informed search) thông minh, kết hợp giữa chi phí thực tế (g(n)) và chi phí ước tính (h(n)) để tìm ra con đường tối ưu nhất.
      Trong bài toán này, các chi phí được định nghĩa như sau:
          - g(n) - Chi phí thực tế: Là số "bước đi" đã thực hiện để đạt đến trạng thái hiện tại. Trong code này, nó được tính là số quân xe đã được đặt đúng vị trí, cộng thêm 1 cho mỗi lần thử một cột sai trong hàng hiện tại.
          - h(n) - Chi phí ước tính (Heuristic): Là một ước tính về chi phí để đi từ trạng thái hiện tại đến đích. Heuristic được sử dụng ở đây rất đơn giản và hiệu quả: nó chính là số quân xe còn lại cần phải đặt để hoàn thành mục tiêu.
      Hoạt ảnh sẽ mô phỏng quá trình tìm kiếm như sau:
          - Thuật toán sẽ duyệt qua các cột một cách tuần tự cho mỗi hàng (tương tự như BFS).    
          - Tại mỗi bước "thử" một quân xe vào một cột, nhãn "Chi phí (Cost)" trên giao diện sẽ hiển thị giá trị g(n) tại thời điểm đó. Bạn có thể thấy chi phí này tăng lên cho mỗi lần thử sai.
          - Khi một quân xe được đặt vào đúng cột của hàng hiện tại (khớp với goal), nó sẽ được "chốt" lại, và thuật toán chuyển sang hàng tiếp theo.
          - Quá trình tiếp tục cho đến khi tất cả các quân xe được đặt đúng vị trí, lúc đó chi phí cuối cùng sẽ bằng tổng số quân xe.
![Giao diện mô phỏng Astar][(Image_Readme/Astar.png)](https://github.com/ngiempv/AI_CaNhan/blob/main/Image_Readme/Astar.png)
   ## Greedy: 
       Thuật toán Greedy (Tham lam) là một thuật toán tìm kiếm có thông tin, luôn ưu tiên lựa chọn con đường có vẻ tốt nhất tại thời điểm hiện tại. Nó ra quyết định chỉ dựa vào giá trị của hàm heuristic h(n) (chi phí ước tính đến đích) mà bỏ qua hoàn toàn chi phí đã đi g(n).
       Trong mô phỏng này, heuristic được định nghĩa một cách trực quan:
          - h(n) - Chi phí ước tính: Là số quân xe còn lại cần phải đặt để đến được trạng thái đích.
          - Một trạng thái được coi là "tốt hơn" nếu nó có giá trị h(n) thấp hơn, tức là gần với lời giải cuối cùng hơn.
![Giao diện mô phỏng Greedy][(Image_Readme/gree.png)](https://github.com/ngiempv/AI_CaNhan/blob/main/Image_Readme/gree.png)
          - Như trên hình ảnh: Cost được tính bằng (8 - số quân xe đã được đặt hợp lệ goal trên bàn cờ). Càng bé càng gần goal
# Tìm kiếm cục bộ (Local):
   ## Hill Climbing: 
       Thuật toán Leo đồi là một vòng lặp đơn giản, liên tục di chuyển theo hướng "dốc lên" (hướng có giá trị tốt hơn).
       Đối với mỗi hàng, thuật toán bắt đầu bằng cách đặt một quân xe vào một cột ngẫu nhiên. Nó kiểm tra hai ô hàng xóm (trái và phải) và di chuyển đến ô nào có chi phí thấp hơn (gần cột đích hơn). Quá trình "leo dốc" này tiếp tục cho đến khi quân xe đến được đúng cột đích của hàng đó (chi phí bằng 0). Sau đó, thuật toán chuyển sang hàng tiếp theo và lặp lại quá trình.
  ## SA: 
    Tôi luyện mô phỏng là một phiên bản cải tiến của Leo đồi, lấy cảm hứng từ quá trình tôi luyện kim loại.
     - Cách Triển Khai
        Năng lượng (Energy): Tương tự như chi phí trong Leo đồi, là khoảng cách đến cột đích.
        Nhiệt độ (Temperature): Một biến số giảm dần theo thời gian. Khi nhiệt độ cao, thuật toán có xu hướng chấp nhận các nước đi tệ nhiều hơn (khám phá nhiều hơn). Khi nhiệt độ giảm, nó trở nên "tham lam" hơn và chỉ chấp nhận các nước đi tốt.
       Hàm xác suất chấp nhận: Một nước đi tệ hơn (với energy_delta > 0) có thể được chấp nhận với xác suất e 
−ΔE/T, trong đó ΔE là sự thay đổi năng lượng và T là nhiệt độ hiện tại.
    - Trực Quan Hóa
    Giống như Leo đồi, thuật toán bắt đầu ở một cột ngẫu nhiên. Tuy nhiên, thay vì luôn đi đến hàng xóm tốt nhất, nó chọn một hàng xóm ngẫu nhiên.
Nếu hàng xóm đó tốt hơn, nó sẽ di chuyển đến đó.
Nếu hàng xóm đó tệ hơn, nó vẫn có thể di chuyển đến đó với một xác suất nhỏ, tạo ra những bước đi có vẻ "ngược đời" nhưng giúp nó khám phá toàn bộ không gian trạng thái.
Hoạt ảnh cho thấy quân xe di chuyển qua lại, dần dần "lắng xuống" vị trí chính xác khi "nhiệt độ" giảm.
  ## GA: 
      Thuật toán Di truyền mô phỏng quá trình tiến hóa và chọn lọc tự nhiên. Nó hoạt động trên một "quần thể" các giải pháp tiềm năng
    - Cách Triển Khai
        Cá thể (Individual): Trong mô phỏng này, một "cá thể" là một cặp cột, đại diện cho vị trí của hai quân xe ở hai hàng liên tiếp.
        Quần thể (Population): Một tập hợp các cá thể (các cặp cột khả thi).
        Độ thích nghi (Fitness): Một hàm để chấm điểm mức độ "tốt" của một cá thể. Ở đây, độ thích nghi được tính dựa trên tổng khoảng cách từ mỗi cột trong cặp đến cột đích tương ứng.
        Chọn lọc: Thuật toán chọn ra cá thể có độ thích nghi cao nhất từ quần thể.
     - Trực Quan Hóa: Thuật toán xử lý hai hàng cùng một lúc. Nó tạo ra một quần thể gồm các cặp cột khả thi và hiển thị chúng dưới dạng các quân xe màu xanh lam. Nó đánh giá tất cả các cặp trong quần thể và chọn ra cặp tốt nhất (gần với goal nhất).
Cặp tốt nhất này được "chốt" lại, và thuật toán chuyển sang hai hàng tiếp theo.
![Giao diện mô phỏng quần thể và cặp con thành công xét theo từng cặp dòng][(Image_Readme/GA.png)](https://github.com/ngiempv/AI_CaNhan/blob/main/Image_Readme/GA.png)
  ## BeamSearch: 
    Tìm kiếm Chùm là một biến thể của tìm kiếm Best-First, nhưng nó chỉ giữ lại một số lượng giới hạn (k, hay BEAM_WIDTH) các trạng thái hứa hẹn nhất ở mỗi bước để khám phá tiếp.
  - Cách Triển Khai: Chùm (Beam): Một danh sách chứa k trạng thái (cột) tốt nhất hiện tại.
                      Đánh giá: Các trạng thái được đánh giá dựa trên chi phí (khoảng cách đến cột đích).
  - Trực Quan Hóa: Tại mỗi hàng, thuật toán xem xét tất cả các cột còn trống. Nó sắp xếp chúng dựa trên khoảng cách đến cột đích và chọn ra BEAM_WIDTH (trong code là 3) cột tốt nhất. "Chùm" gồm 3 ứng viên này được hiển thị bằng các quân xe màu xanh lam.
Từ trong chùm, thuật toán chọn ra quân xe tốt nhất tuyệt đối, "chốt" nó lại bằng màu đỏ, và chuyển sang hàng tiếp theo.
![Giao diện mô phỏng các bước tốt nhất và tìm ra goal theo từng dòng của BeamSearch][(Image_Readme/beam.png)](https://github.com/ngiempv/AI_CaNhan/blob/main/Image_Readme/beam.png)
  ## AndOrSearch: 
    Thuật toán AND-OR Search được sử dụng để giải quyết các bài toán có thể được phân rã thành các bài toán con
    - Cách Triển Khai & Trực Quan Hóa
    Hoạt ảnh mô phỏng quá trình này một cách trực quan: Đối với mỗi hàng (một nhánh AND), thuật toán sẽ thử lần lượt các cột (các nhánh OR).Các quân xe đã được "chốt" vị trí (đại diện cho các nhánh AND đã thành công) sẽ có màu đỏ. 
Quân xe đang được thử nghiệm ở hàng hiện tại (một nhánh OR) sẽ có màu xanh lam.  Thuật toán sẽ duyệt qua các quân xe màu xanh cho đến khi tìm thấy vị trí khớp với goal. Khi một nhánh OR thành công, quân xe sẽ được "chốt" lại thành màu đỏ, và thuật toán chuyển sang giải quyết nhánh AND tiếp theo (hàng tiếp theo).
![Giao diện mô phỏng các bước and đã được chấp nhận và or khi đang xét trong thuật toán][(Image_Readme/andor.png)](https://github.com/ngiempv/AI_CaNhan/blob/main/Image_Readme/andor.png)
  ## Belief State: 
        Belief State Search là một khái niệm dùng cho các tác tử hoạt động trong môi trường không chắc chắn hoặc chỉ quan sát được một phần.
      - Cách Triển Khai & Trực Quan Hóa
          Xác định Belief State: Tại mỗi hàng, "trạng thái niềm tin" của thuật toán là tập hợp tất cả các cột còn trống mà quân xe có thể được đặt vào.
      - Hiển thị:
          Các quân xe đã được đặt chính xác sẽ có màu đỏ.
          Tất cả các vị trí trong "trạng thái niềm tin" ở hàng hiện tại sẽ được hiển thị bằng các quân xe màu xám.
          Cập nhật Niềm tin (Belief Update): Sau khi hiển thị tất cả các khả năng, thuật toán sẽ "quan sát" và xác định được vị trí đúng (vị trí goal).
          "Sụp đổ" Trạng thái: Hoạt ảnh sẽ xóa tất cả các quân xe màu xám và "chốt" lại quân xe đúng bằng màu đỏ. Quá trình này mô phỏng việc loại bỏ sự không chắc chắn và cập nhật lại "niềm tin" của tác tử.
          Thuật toán sau đó chuyển sang hàng tiếp theo với một "trạng thái niềm tin" mới.
![Giao diện mô phỏng niềm tin bằng các con xe màu xám][(Image_Readme/belir.png)](https://github.com/ngiempv/AI_CaNhan/blob/main/Image_Readme/beli.png)
  ## Back tracking Search: 
        Thuật toán cơ bản và mạnh mẽ để giải quyết CSP. Nó xây dựng giải pháp một cách có hệ thống, từng bước một. Ngay khi xác định một bước đi vi phạm ràng buộc, nó sẽ "quay lui" (backtrack) để thử một lựa chọn khác, qua đó tránh phải duyệt qua các nhánh tìm kiếm vô ích.
      - Cách Triển Khai & Trực Quan Hóa:
          Thuật toán bắt đầu từ hàng đầu tiên và thử đặt một quân xe vào từng cột.
          Kiểm tra Ràng buộc (is_safe): Sau mỗi lần thử, nó kiểm tra xem vị trí mới có bị tấn công bởi các quân xe đã đặt ở các hàng trước đó không.
          Đi sâu hơn: Nếu vị trí là an toàn, nó sẽ gọi đệ quy để giải quyết cho hàng tiếp theo.
          Quay lui: Nếu một nhánh tìm kiếm dẫn đến ngõ cụt (không tìm được vị trí an toàn cho hàng tiếp theo), hàm đệ quy sẽ trả về thất bại. Hoạt ảnh sẽ cho thấy quân xe ở bước thử sai bị xóa đi, và thuật toán sẽ thử cột tiếp theo trong hàng hiện tại. Đây chính là hành động "quay lui" được trực quan hóa.
Quá trình này tiếp tục cho đến khi tìm thấy một cấu hình hoàn chỉnh khớp với trạng thái đích.
  ## Forward Checking: 
    Một phiên bản cải tiến và thông minh hơn của Backtracking.
      - Cách Triển Khai:
            Miền giá trị (Domain): Mỗi hàng "tương lai" (chưa được đặt xe) có một "miền giá trị" – là tập hợp các cột mà quân xe có thể được đặt vào.
            Kiểm tra trước: Khi thuật toán đặt một quân xe vào vị trí (hàng, cột), nó sẽ ngay lập tức loại bỏ cột đó ra khỏi miền giá trị của tất cả các hàng trong tương lai.  
            Phát hiện ngõ cụt sớm: Nếu việc loại bỏ này khiến cho miền giá trị của một hàng tương lai bất kỳ trở nên rỗng, thuật toán biết ngay rằng đây là một ngõ cụt và sẽ quay lui ngay lập tức, mà không cần phải đi sâu xuống nhánh đó.
         -  Trực Quan Hóa
            Giống như Backtracking, các quân xe đã được "chốt" sẽ có màu đỏ.
            Điểm khác biệt chính là sự xuất hiện của các dấu '✕' màu xám trên bàn cờ.
Các dấu '✕' này đại diện cho các ô đã bị loại khỏi miền giá trị của các hàng tương lai do các quyết định đã đưa ra. Hoạt ảnh cho thấy rõ cách không gian tìm kiếm được "cắt tỉa" một cách chủ động, giúp thuật toán tìm ra lời giải hiệu quả hơn so với Backtracking thông thường: ![Giao diện mô phỏng đại diện cho các ô bị loại khỏi miền giá trị][(Image_Readme/forCheck.png)](https://github.com/ngiempv/AI_CaNhan/blob/main/Image_Readme/forCheck.png)
