import tkinter as tk
import random
from collections import deque
import heapq # Cần cho UCS
import math
import itertools

SIZE = 8
SqSize = 60

LIGHT_COLOR = "#FFFFFF"
DARK_COLOR = "#000000"

# --- BIẾN TOÀN CỤC CHO ANIMATION ---
after_id = None 
confirmed_car = []
current_search_row = 0
goal_map = {}
# Biến riêng cho từng thuật toán
col_queue = deque() # Hàng đợi cho BFS
col_stack = []      # Ngăn xếp cho DFS

def chessboard(board, sx, sy):
    for i in range(SIZE):
        for j in range(SIZE):
            x1 = sx + j * SqSize
            y1 = sy + i * SqSize
            x2 = x1 + SqSize
            y2 = y1 + SqSize
            color = LIGHT_COLOR if (i + j) % 2 == 0 else DARK_COLOR
            board.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

def drawcar(board, sx, sy, positions, color="red", tag=""):
    board.delete(tag) 
    for row, col in positions:
        x = sx + col * SqSize + SqSize // 2
        y = sy + row * SqSize + SqSize // 2
        board.create_text(x, y, text="♖", font=("Arial", 24), fill=color, tags=tag)

# BFS
def run_bfs():
    global confirmed_car, current_search_row, goal_map, col_queue
    if not right_positions: status_label.config(text="Lỗi: Hãy đặt quân xe ở bàn phải làm goal!"); return
    confirmed_car, current_search_row = [], 0; goal_map = {r: c for r, c in sorted(right_positions)}
    col_queue.clear(); col_queue.extend(range(SIZE)); animate_bfs_step()

def animate_bfs_step():
    global after_id, current_search_row, col_queue, confirmed_car, goal_map, left_positions
    if len(confirmed_car) == len(goal_map): status_label.config(text="BFS: Đã hoàn thành!"); return
    if not col_queue: return
    trial_col = col_queue.popleft()
    car_to_draw = confirmed_car + [(current_search_row, trial_col)]
    left_positions = car_to_draw; drawcar(board, 0, 0, car_to_draw, "red", "left_car"); board.update_idletasks()
    target_col = goal_map.get(current_search_row)
    if trial_col == target_col:
        confirmed_car.append((current_search_row, trial_col)); current_search_row += 1
        if current_search_row < len(goal_map): col_queue.clear(); col_queue.extend(range(SIZE))
    after_id = board.after(100, animate_bfs_step)

# DFS
def run_dfs():
    global confirmed_car, current_search_row, goal_map, col_stack
    if not right_positions: status_label.config(text="Lỗi: Hãy đặt quân xe ở bàn phải làm goal!"); return
    confirmed_car, current_search_row = [], 0; goal_map = {r: c for r, c in sorted(right_positions)}
    col_stack.clear(); col_stack.extend(range(SIZE)); animate_dfs_step()

def animate_dfs_step():
    global after_id, current_search_row, col_stack, confirmed_car, goal_map, left_positions
    if len(confirmed_car) == len(goal_map): status_label.config(text="DFS: Đã hoàn thành!"); return
    if not col_stack: return
    trial_col = col_stack.pop()
    car_to_draw = confirmed_car + [(current_search_row, trial_col)]
    left_positions = car_to_draw; drawcar(board, 0, 0, car_to_draw, "red", "left_car"); board.update_idletasks()
    target_col = goal_map.get(current_search_row)
    if trial_col == target_col:
        confirmed_car.append((current_search_row, trial_col)); current_search_row += 1
        if current_search_row < len(goal_map): col_stack.clear(); col_stack.extend(range(SIZE))
    after_id = board.after(100, animate_dfs_step)

# UCS/DLS
def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def calculate_path(path):
    # Tính tổng chi phí của một đường đi dựa trên khoảng cách Manhattan
    if len(path) < 2:
        return 0
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += manhattan(path[i], path[i+1])
    return total_cost

def run_ucs():
    global confirmed_car, current_search_row, goal_map, col_queue
    if not right_positions: status_label.config(text="Lỗi: Hãy đặt quân xe ở bàn phải làm goal!"); return
    confirmed_car, current_search_row = [], 0
    goal_map = {r: c for r, c in sorted(right_positions)}
    col_queue.clear(); col_queue.extend(range(SIZE)); animate_ucs_step()

def animate_ucs_step():
    global after_id, current_search_row, col_queue, confirmed_car, goal_map, left_positions
    if len(confirmed_car) == len(goal_map): status_label.config(text="UCS: Đã hoàn thành!"); return
    if not col_queue: return

    trial_col = col_queue.popleft()
    car_to_draw = confirmed_car + [(current_search_row, trial_col)]
    left_positions = car_to_draw
    
    # Vẽ và cập nhật chi phí
    drawcar(board, 0, 0, car_to_draw, "red", "left_car")
    cost = calculate_path(car_to_draw)
    cost_value_label.config(text=str(cost))
    board.update_idletasks()

    target_col = goal_map.get(current_search_row)
    if trial_col == target_col:
        confirmed_car.append((current_search_row, trial_col))
        current_search_row += 1
        if current_search_row < len(goal_map):
            col_queue.clear(); col_queue.extend(range(SIZE))
    after_id = board.after(100, animate_ucs_step)

def run_dls():
    global confirmed_car, current_search_row, goal_map, col_stack
    if not right_positions:
        status_label.config(text="Lỗi: Hãy đặt quân xe ở bàn phải làm goal!")
        return

    confirmed_car = []
    current_search_row = 0
    goal_map = {r: c for r, c in sorted(right_positions)}
    col_stack = list(range(SIZE))   # đảm bảo khởi tạo mới
    animate_dls_step()

def animate_dls_step(limit=SIZE):
    global after_id, current_search_row, col_stack, confirmed_car, goal_map, left_positions

    # 1. Kiểm tra giới hạn độ sâu
    if current_search_row >= limit:
        status_label.config(text=f"DLS: Đạt giới hạn độ sâu {limit}")
        return

    # 2. Kiểm tra goal
    if len(confirmed_car) == len(goal_map):
        status_label.config(text="DLS: Đã hoàn thành!")
        return

    # 3. Nếu stack rỗng → reset
    if not col_stack:
        col_stack.extend(range(SIZE))
        current_search_row += 1
        if current_search_row >= limit:
            status_label.config(text=f"DLS: Hết độ sâu {limit}")
            return

    # 4. Lấy cột cần thử
    trial_col = col_stack.pop()
    car_to_draw = confirmed_car + [(current_search_row, trial_col)]
    left_positions = car_to_draw

    # 5. Vẽ
    drawcar(board, 0, 0, car_to_draw, "red", "left_car")
    board.update_idletasks()

    # 6. Nếu đúng goal ở hàng này → xác nhận
    target_col = goal_map.get(current_search_row)
    if trial_col == target_col:
        confirmed_car.append((current_search_row, trial_col))
        current_search_row += 1
        col_stack.clear()
        col_stack.extend(range(SIZE))

    # 7. Lên lịch bước tiếp
    after_id = board.after(300, lambda: animate_dls_step(limit))

# IDS
def run_ids():
    """Hàm quản lý vòng lặp IDS."""
    global goal_map, ids_current_limit
    if not right_positions:
        status_label.config(text="Lỗi: Hãy đặt quân xe ở bàn phải làm goal!")
        return
    
    goal_map = {row: col for row, col in sorted(right_positions)}
    ids_current_limit = 1 # Bắt đầu lặp với giới hạn độ sâu là 1
    start_ids_iteration()

def start_ids_iteration():
    """Bắt đầu một lần tìm kiếm DLS trong chuỗi IDS."""
    global confirmed_car, current_search_row, col_stack
    
    status_label.config(text=f"IDS: Bắt đầu tìm kiếm với giới hạn {ids_current_limit}...")
    
    # Reset trạng thái cho lần tìm kiếm mới
    confirmed_car, current_search_row = [], 0
    col_stack.clear()
    col_stack.extend(range(SIZE))
    
    # Gọi hàm animation riêng của IDS
    board.after(1000, animate_ids_step) 

def animate_ids_step():
    """Animation step dành riêng cho IDS."""
    global after_id, current_search_row, col_stack, confirmed_car, goal_map, left_positions, ids_current_limit

    # Điều kiện dừng: Đã tìm đủ quân cờ cho giới hạn hiện tại
    if len(confirmed_car) == ids_current_limit:
        status_label.config(text=f"IDS: Hoàn thành ở độ sâu {ids_current_limit}.")
        
        # Nếu chưa phải goal cuối cùng, tăng giới hạn và lặp lại
        if ids_current_limit < len(goal_map):
            ids_current_limit += 1
            board.delete("left_car") # Xóa bàn cờ để bắt đầu lại
            start_ids_iteration() # Bắt đầu vòng lặp mới
        else:
            status_label.config(text="IDS: Đã tìm thấy goal cuối cùng!")
        return # Dừng lần chạy DLS hiện tại

    # Logic tìm kiếm của DLS (giống DFS)
    if not col_stack: 
        # Nếu hết cột để thử mà chưa đạt limit, nghĩa là lần lặp này thất bại
        status_label.config(text=f"IDS: Thất bại ở độ sâu {ids_current_limit}. Tăng giới hạn...")
        ids_current_limit += 1
        board.delete("left_car")
        start_ids_iteration()
        return

    trial_col = col_stack.pop()
    car_to_draw = confirmed_car + [(current_search_row, trial_col)]
    left_positions = car_to_draw
    drawcar(board, 0, 0, car_to_draw, "red", "left_car")
    board.update_idletasks()
    target_col = goal_map.get(current_search_row)

    if trial_col == target_col:
        confirmed_car.append((current_search_row, trial_col))
        current_search_row += 1
        if current_search_row < len(goal_map):
            col_stack.clear()
            col_stack.extend(range(SIZE))
    
    after_id = board.after(100, animate_ids_step)

# A* Search
def heuristic(state_len, goal_len):
    return goal_len - state_len

def run_a_star():
    global confirmedcar, current_search_row, goal_map, col_queue
    if not right_positions: 
        status_label.config(text="Lỗi: Hãy đặt quân xe ở bàn phải làm goal!")
        return
    # Chuẩn bị 
    confirmedcar, current_search_row = [], 0
    goal_map = {r: c for r, c in sorted(right_positions)}
    col_queue.clear()
    col_queue.extend(range(SIZE))
    animate_as_step()
def animate_as_step():
    global after_id, current_search_row, col_queue, confirmedcar, goal_map, left_positions
    
    # Điều kiện dừng
    if len(confirmedcar) == len(goal_map): 
        status_label.config(text="A*: Đã hoàn thành!")
        # Chi phí cuối cùng là số quân xe đã đặt
        cost_value_label.config(text=str(len(confirmedcar)))
        return
    if not col_queue: return
    trial_col = col_queue.popleft()
    car_to_draw = confirmedcar + [(current_search_row, trial_col)]
    left_positions = car_to_draw
    
    # A* LOgic
    # g(n) là chi phí thực tế: số quân xe đã "chốt" vị trí.
    g = len(confirmedcar)
    # Nếu bước thử hiện tại chưa phải là bước đúng, chi phí thực tế của đường đi này tăng thêm 1
    if trial_col != goal_map.get(current_search_row):
        g += 1
        
    # h(n) là chi phí ước tính: số quân xe còn lại cần đặt để tới goal.
    h = heuristic(len(confirmedcar), len(goal_map))

    # f(n) = g(n) + h(n). Chúng ta sẽ hiển thị chi phí thực tế g(n)
    cost_value_label.config(text=str(g))
    
    # --- Vẽ và cập nhật giao diện ---
    drawcar(board, 0, 0, car_to_draw, "red", "left_car")
    board.update_idletasks()

    # So sánh và chuyển sang dòng tiếp theo (giống BFS)
    target_col = goal_map.get(current_search_row)
    if trial_col == target_col:
        confirmedcar.append((current_search_row, trial_col))
        current_search_row += 1
        if current_search_row < len(goal_map):
            col_queue.clear()
            col_queue.extend(range(SIZE))
    
    after_id = board.after(100, animate_as_step)

# Greedy Search
def run_greedy():
    global confirmedcar, current_search_row, goal_map, col_stack
    if not right_positions: status_label.config(text="Lỗi: Hãy đặt quân xe ở bàn phải làm goal!"); return
    confirmedcar, current_search_row = [], 0
    goal_map = {r: c for r, c in sorted(right_positions)}
    col_stack.clear(); col_stack.extend(range(SIZE)); animate_greedy_step()
def animate_greedy_step():
    global after_id, current_search_row, col_stack, confirmedcar, goal_map, left_positions
    if len(confirmedcar) == len(goal_map): 
        status_label.config(text="Greedy: Đã hoàn thành!")
        cost_value_label.config(text="0") # Chi phí heuristic cuối cùng là 0
        return
    if not col_stack: return

    trial_col = col_stack.pop()
    car_to_draw = confirmedcar + [(current_search_row, trial_col)]
    left_positions = car_to_draw
    
    # LOgic Greedy
    # Cost hiển thị là giá trị heuristic h(n)
    h = heuristic(len(confirmedcar), len(goal_map))
    cost_value_label.config(text=str(h))
    
    # Vẽ và cập nhật giao diện
    drawcar(board, 0, 0, car_to_draw, "red", "left_car")
    board.update_idletasks()

    target_col = goal_map.get(current_search_row)
    if trial_col == target_col:
        confirmedcar.append((current_search_row, trial_col))
        current_search_row += 1
        if current_search_row < len(goal_map):
            col_stack.clear(); col_stack.extend(range(SIZE))
    
    after_id = board.after(100, animate_greedy_step)
# Local search 
# Hill climbing
def hill_climbing(state, n=SIZE):
    global confirmedcar, current_search_row, goal_map, hill_climbing_current_col
    if not right_positions: 
        status_label.config(text="Lỗi: Hãy đặt quân xe ở bàn phải làm goal!")
        return
    confirmedcar, current_search_row = [], 0
    goal_map = {r: c for r, c in sorted(right_positions)}
    # Bắt đầu ở một cột ngẫu nhiên cho dòng đầu tiên
    hill_climbing_current_col = random.randint(0, SIZE - 1)
    animate_hill_climbing_step()

def animate_hill_climbing_step():
    global after_id, current_search_row, hill_climbing_current_col, confirmedcar, goal_map, left_positions

    if len(confirmedcar) == len(goal_map):
        status_label.config(text="Hill Climbing: Đã hoàn thành!")
        return

    # Lấy cột goal của dòng hiện tại
    target_col = goal_map.get(current_search_row)
    
    # Vẽ trạng thái "thử" hiện tại
    car_to_draw = confirmedcar + [(current_search_row, hill_climbing_current_col)]
    left_positions = car_to_draw
    drawcar(board, 0, 0, car_to_draw, "red", "left_car")
    board.update_idletasks()

    # Tính chi phí (khoảng cách đến goal)
    current_cost = abs(hill_climbing_current_col - target_col)
    cost_value_label.config(text=str(current_cost))

    # Nếu đã ở vị trí tốt nhất (goal), chốt và chuyển sang dòng tiếp theo
    if current_cost == 0:
        confirmedcar.append((current_search_row, hill_climbing_current_col))
        current_search_row += 1
        if current_search_row < len(goal_map):
            # Bắt đầu ở vị trí ngẫu nhiên cho dòng mới
            hill_climbing_current_col = random.randint(0, SIZE - 1)
        after_id = board.after(200, animate_hill_climbing_step)
        return

    # Tìm hàng xóm tốt hơn
    best_neighbor_col = hill_climbing_current_col
    best_neighbor_cost = current_cost
    
    # Kiểm tra hàng xóm bên trái
    if hill_climbing_current_col > 0:
        left_neighbor_cost = abs((hill_climbing_current_col - 1) - target_col)
        if left_neighbor_cost < best_neighbor_cost:
            best_neighbor_cost = left_neighbor_cost
            best_neighbor_col = hill_climbing_current_col - 1
            
    # Kiểm tra hàng xóm bên phải
    if hill_climbing_current_col < SIZE - 1:
        right_neighbor_cost = abs((hill_climbing_current_col + 1) - target_col)
        if right_neighbor_cost < best_neighbor_cost:
            best_neighbor_cost = right_neighbor_cost
            best_neighbor_col = hill_climbing_current_col + 1

    # Di chuyển đến hàng xóm tốt hơn
    hill_climbing_current_col = best_neighbor_col
    after_id = board.after(200, animate_hill_climbing_step)
# Simulated Annealing
def simulated_annealing():
    global confirmed_car, current_search_row, goal_map, current_col, temperature
    if not right_positions: 
        status_label.config(text="Lỗi: Hãy đặt quân xe ở bàn phải làm goal!")
        return
    
    confirmed_car, current_search_row = [], 0
    goal_map = {r: c for r, c in sorted(right_positions)}
    # Bắt đầu ở một cột ngẫu nhiên và reset nhiệt độ
    current_col = random.randint(0, SIZE - 1)
    temperature = 10000
    animate_simulated_annealing_step()
def animate_simulated_annealing_step():
    global after_id, current_search_row, current_col, confirmed_car, goal_map, left_positions, temperature

    if len(confirmed_car) == len(goal_map):
        status_label.config(text="Simulated Annealing: Đã hoàn thành!")
        return

    target_col = goal_map.get(current_search_row)
    
    # Vẽ trạng thái hiện tại
    car_to_draw = confirmed_car + [(current_search_row, current_col)]
    left_positions = car_to_draw
    drawcar(board, 0, 0, car_to_draw, "red", "left_car")
    board.update_idletasks()

    # Tính "năng lượng" (chi phí) của trạng thái hiện tại
    current_energy = abs(current_col - target_col)
    cost_value_label.config(text=str(current_energy))

    # Nếu đã đạt goal cho dòng này, chốt và chuyển sang dòng tiếp theo
    if current_energy == 0:
        confirmed_car.append((current_search_row, current_col))
        current_search_row += 1
        if current_search_row < len(goal_map):
            current_col = random.randint(0, SIZE - 1)
            temperature = 10000 # Reset nhiệt độ cho dòng mới
        after_id = board.after(200, animate_simulated_annealing_step)
        return

    # Chọn một hàng xóm ngẫu nhiên (trái hoặc phải)
    neighbors = []
    if current_col > 0: neighbors.append(current_col - 1)
    if current_col < SIZE - 1: neighbors.append(current_col + 1)
    
    if not neighbors: 
        after_id = board.after(100, animate_simulated_annealing_step)
        return

    next_col = random.choice(neighbors)
    next_energy = abs(next_col - target_col)
    
    # Quyết định có di chuyển hay không
    energy_delta = next_energy - current_energy
    if energy_delta < 0 or (temperature > 0 and random.uniform(0, 1) < math.exp(-energy_delta / temperature)):
        current_col = next_col 

    # --- ĐÂY LÀ DÒNG LỆNH ĐÃ SỬA ---
    temperature *= 0.99 
    
    after_id = board.after(100, animate_simulated_annealing_step)
# Genetic Algorithm
# Biến GA
opulation = []
generation_count = 0
POPULATION_SIZE = 50
MUTATION_RATE = 0.1
current_col_pair = () # Cặp cha mẹ hiện tại để lai tạo
    # Tạo ra một quần thể ban đầu gồm các cá thể ngẫu nhiên.
def run_ga():
    global confirmed_car, current_search_row, goal_map, current_col_pair
    if not right_positions or len(right_positions) % 2 != 0: 
        status_label.config(text="Lỗi: GA cần số lượng goal chẵn!")
        return
    
    confirmed_car, current_search_row = [], 0
    goal_map = {r: c for r, c in sorted(right_positions)}
    
    # Bắt đầu với một cặp cột ngẫu nhiên hợp lệ
    used_cols = [c for r,c in confirmed_car]
    available_cols = [c for c in range(SIZE) if c not in used_cols]
    current_col_pair = random.sample(available_cols, 2)
    
    animate_ga_step()
# Thực hiện một bước tiến hóa của GA trên một cặp dòng.
def animate_ga_step():
    
    global after_id, current_search_row, current_col_pair, confirmed_car, goal_map, left_positions

    if len(confirmed_car) == len(goal_map):
        status_label.config(text="Genetic Algorithm: Đã hoàn thành!")
        return

    # Lấy goal cho cặp dòng hiện tại
    target_col1 = goal_map.get(current_search_row)
    target_col2 = goal_map.get(current_search_row + 1)
    
    # Nếu cặp hiện tại đã đúng, chốt lại và chuyển sang cặp dòng tiếp theo
    if current_col_pair[0] == target_col1 and current_col_pair[1] == target_col2:
        confirmed_car.append((current_search_row, current_col_pair[0]))
        confirmed_car.append((current_search_row + 1, current_col_pair[1]))
        current_search_row += 2 # Bước nhảy là 2
        
        drawcar(board, 0, 0, confirmed_car, color="red", tag="left_car")
        board.update_idletasks()

        if current_search_row < len(goal_map):
            used_cols = [c for r,c in confirmed_car]
            available_cols = [c for c in range(SIZE) if c not in used_cols]
            current_col_pair = random.sample(available_cols, 2)
            after_id = board.after(500, animate_ga_step)
        else:
            status_label.config(text="Genetic Algorithm: Đã hoàn thành!")
        return

    # --- LOGIC CỦA GA ---
    # 1. Tạo "quần thể" các cặp cột mới
    population_size = 10 
    used_cols = [c for r,c in confirmed_car]
    available_cols = [c for c in range(SIZE) if c not in used_cols]
    
    # Lấy tất cả các cặp có thể từ các cột còn lại
    all_possible_pairs = list(itertools.combinations(available_cols, 2))
    population = random.sample(all_possible_pairs, min(len(all_possible_pairs), population_size))
    
    # 2. Hiển thị các cặp ứng viên
    board.delete("ga_candidate")
    candidate_positions = []
    for col_pair in population:
        candidate_positions.append((current_search_row, col_pair[0]))
        candidate_positions.append((current_search_row + 1, col_pair[1]))
    
    drawcar(board, 0, 0, confirmed_car, color="red", tag="left_car")
    drawcar(board, 0, 0, candidate_positions, color="#007BFF", tag="ga_candidate")
    board.update_idletasks()
    
    # 3. Đánh giá và chọn cặp tốt nhất
    best_pair = None
    best_fitness = -1
    for col_pair in population:
        # Fitness càng cao càng tốt (tổng khoảng cách đến goal càng nhỏ)
        fitness1 = SIZE - abs(col_pair[0] - target_col1)
        fitness2 = SIZE - abs(col_pair[1] - target_col2)
        total_fitness = fitness1 + fitness2
        if total_fitness > best_fitness:
            best_fitness = total_fitness
            best_pair = col_pair
    
    # 4. Cập nhật trạng thái
    current_col_pair = best_pair
    cost = (SIZE - (SIZE - abs(best_pair[0] - target_col1))) + (SIZE - (SIZE - abs(best_pair[1] - target_col2)))
    cost_value_label.config(text=str(cost))
    
    board.after(400, lambda: board.delete("ga_candidate"))
    after_id = board.after(600, animate_ga_step)
# Beam seảrch
BEAM_WIDTH = 3
def beam_search():
    global confirmed_car, current_search_row, goal_map
    if not right_positions: 
        status_label.config(text="Lỗi: Hãy đặt quân xe ở bàn phải làm goal!")
        return
    
    confirmed_car, current_search_row = [], 0
    goal_map = {r: c for r, c in sorted(right_positions)}
    animate_beam_search_step()
def animate_beam_search_step():
    global after_id, current_search_row, confirmed_car, goal_map, left_positions

    if len(confirmed_car) == len(goal_map):
        status_label.config(text="Beam Search: Đã hoàn thành!")
        return

    target_col = goal_map.get(current_search_row)
    
    # --- LOGIC CỦA BEAM SEARCH ---
    # 1. Tạo ra tất cả các trạng thái con có thể
    used_cols = [c for r,c in confirmed_car]
    available_cols = [c for c in range(SIZE) if c not in used_cols]
    
    candidates = []
    for col_option in available_cols:
        # Cost là khoảng cách đến goal
        cost = abs(col_option - target_col)
        candidates.append((cost, col_option))
        
    # 2. Sắp xếp và chọn ra 'k' ứng viên tốt nhất (chùm)
    candidates.sort(key=lambda x: x[0])
    beam = candidates[:BEAM_WIDTH]
    
    # 3. Hiển thị chùm
    board.delete("beam_candidate")
    beam_positions = []
    for _, col_option in beam:
        beam_positions.append((current_search_row, col_option))

    drawcar(board, 0, 0, confirmed_car, color="red", tag="left_car")
    drawcar(board, 0, 0, beam_positions, color="#007BFF", tag="beam_candidate")
    
    # Lấy ra ứng viên tốt nhất tuyệt đối trong chùm
    best_cost, best_col = beam[0]
    cost_value_label.config(text=str(best_cost))
    board.update_idletasks()
    
    # Lên lịch để "chốt" lựa chọn tốt nhất
    after_id = board.after(600, lambda: finalize_beam_choice(best_col))

def finalize_beam_choice(chosen_col):
    global after_id, current_search_row, confirmed_car
    
    board.delete("beam_candidate") # Ẩn chùm
    
    # Chốt lựa chọn
    confirmed_car.append((current_search_row, chosen_col))
    current_search_row += 1
    
    # Vẽ lại bàn cờ với quân xe màu đỏ vừa được chốt
    drawcar(board, 0, 0, confirmed_car, color="red", tag="left_car")
    board.update_idletasks()
    
    # Lên lịch cho dòng tiếp theo
    after_id = board.after(200, animate_beam_search_step)

def run_andor():
    """Chuẩn bị và bắt đầu animation AND-OR Search."""
    global confirmed_car, current_search_row, goal_map, col_queue
    if not right_positions: 
        status_label.config(text="Lỗi: Hãy đặt quân xe ở bàn phải làm goal!")
        return
    
    # Chuẩn bị giống hệt BFS
    confirmed_car, current_search_row = [], 0
    goal_map = {r: c for r, c in sorted(right_positions)}
    col_queue.clear()
    col_queue.extend(range(SIZE)) # Nạp các nhánh OR (các cột) vào hàng đợi
    animate_andor_step()

def animate_andor_step():
    global after_id, current_search_row, col_queue, confirmed_car, goal_map, left_positions

    # Nếu đã giải quyết hết các nhánh AND (các dòng), dừng lại
    if len(confirmed_car) == len(goal_map): 
        status_label.config(text="AND-OR Search: Đã hoàn thành!")
        return
    
    # Nếu đã thử hết các nhánh OR (các cột) mà chưa thành công, dừng lại (lỗi)
    if not col_queue: return

    # Lấy một nhánh OR để thử
    trial_col = col_queue.popleft()
    
    # Vẽ các quân đã chốt (nhánh AND đã thành công) màu đỏ
    # và quân đang thử (nhánh OR) màu xanh
    car_to_draw = confirmed_car + [(current_search_row, trial_col)]
    drawcar(board, 0, 0, confirmed_car, color="red", tag="left_car")
    drawcar(board, 0, 0, [(current_search_row, trial_col)], color="#007BFF", tag="or_branch")
    board.update_idletasks()

    target_col = goal_map.get(current_search_row)
    
    # Nếu nhánh OR này thành công (khớp goal)
    if trial_col == target_col:
        # Chốt nhánh này và chuyển sang nhánh AND tiếp theo (dòng tiếp theo)
        confirmed_car.append((current_search_row, trial_col))
        current_search_row += 1
        
        # Vẽ lại lần cuối bằng màu đỏ để xác nhận
        drawcar(board, 0, 0, confirmed_car, color="red", tag="left_car")
        board.delete("or_branch") # Xóa nhánh OR màu xanh
        board.update_idletasks()
        
        # Nạp các nhánh OR mới cho dòng tiếp theo
        if current_search_row < len(goal_map): 
            col_queue.clear()
            col_queue.extend(range(SIZE))
        
        # Đợi một chút trước khi sang nhánh AND mới
        after_id = board.after(500, animate_andor_step)
    else:
        # Nếu nhánh OR này thất bại, tiếp tục thử nhánh OR khác
        after_id = board.after(100, animate_andor_step)
# Belief State search
def run_beliefS():
    global confirmed_car, current_search_row, goal_map
    if not right_positions: 
        status_label.config(text="Lỗi: Hãy đặt quân xe ở bàn phải làm goal!")
        return
    
    confirmed_car, current_search_row = [], 0
    goal_map = {r: c for r, c in sorted(right_positions)}
    animate_beliefS_step()

def animate_beliefS_step():
    global after_id, current_search_row, confirmed_car, goal_map

    if len(confirmed_car) == len(goal_map):
        status_label.config(text="Belief State: Đã hoàn thành!")
        return

    # 1. Xác định Belief State (tất cả các cột còn trống)
    used_cols = [c for r,c in confirmed_car]
    beliefS_cols = [c for c in range(SIZE) if c not in used_cols]
    
    # 2. Hiển thị Belief State
    board.delete("beliefS")
    belief_positions = []
    for col_option in beliefS_cols:
        belief_positions.append((current_search_row, col_option))

    # Vẽ các quân đã chốt (màu đỏ) và các quân trong belief state (màu xám)
    drawcar(board, 0, 0, confirmed_car, color="red", tag="left_car")
    drawcar(board, 0, 0, belief_positions, color="#CCCCCC", tag="beliefS")
    board.update_idletasks()
    
    # Lấy ra trạng thái đúng từ goal
    target_col = goal_map.get(current_search_row)
    
    # 3. Lên lịch để "sụp đổ" belief state
    after_id = board.after(600, lambda: finalize_belief_choice(target_col))
# Cập nhật niềm tin, chỉ giữ lại trạng thái đúng và chuyển sang dòng tiếp theo.
def finalize_belief_choice(chosen_col):

    global after_id, current_search_row, confirmed_car
    
    board.delete("beliefS") # Ẩn belief state
    
    # Chốt lựa chọn đúng
    confirmed_car.append((current_search_row, chosen_col))
    current_search_row += 1
    
    # Vẽ lại bàn cờ với quân xe màu đỏ vừa được chốt
    drawcar(board, 0, 0, confirmed_car, color="red", tag="left_car")
    cost_value_label.config(text=str(len(confirmed_car)))
    board.update_idletasks()
    
    # Lên lịch cho dòng tiếp theo
    after_id = board.after(200, animate_beliefS_step)
# Backtracking
def is_safe(path, row, col):
    for r, c in enumerate(path):
        # Chỉ cần kiểm tra xem có quân xe nào khác trên cùng cột không
        if c == col:
            return False
    # Không cần kiểm tra đường chéo cho quân xe
    return True

def run_backtracking():
    global confirmed_car, goal_map
    if not right_positions:
        status_label.config(text="Lỗi: Hãy đặt goal ở bàn phải để so sánh!")
        return

    status_label.config(text="Backtracking: Đang truy tìm goal...")
    confirmed_car = [] # Biến này không thực sự được dùng, nhưng reset cho an toàn
    goal_map = {r: c for r, c in sorted(right_positions)}

    # Bắt đầu quá trình tìm kiếm đệ quy từ bàn cờ trống
    animate_backtracking_step([])

def animate_backtracking_step(path):
    global after_id, left_positions

    # 1. Vẽ trạng thái hiện tại
    positions_to_draw = [(r, c) for r, c in enumerate(path)]
    left_positions = positions_to_draw
    drawcar(board, 0, 0, positions_to_draw, "red", "left_car")
    cost_value_label.config(text=str(len(path)))
    board.update_idletasks()

    # 2. Điều kiện dừng: Nếu đã tìm thấy một lời giải hoàn chỉnh
    if len(path) == SIZE:
        # So sánh lời giải tìm được với goal
        found_solution_map = {r: c for r, c in enumerate(path)}

        # Nếu khớp goal, báo thành công và dừng lại
        if found_solution_map == goal_map:
            status_label.config(text="Backtracking: Đã tìm thấy goal!")
            return True # Báo hiệu đã tìm thấy lời giải, dừng toàn bộ đệ quy
        else:
            # Nếu không khớp, coi như ngõ cụt và quay lui để tìm tiếp
            return False

    # 3. Thử các lựa chọn cho dòng tiếp theo
    next_row = len(path)
    for col in range(SIZE):
        # Hiển thị bước "thử"
        trial_positions = positions_to_draw + [(next_row, col)]
        drawcar(board, 0, 0, trial_positions, "red", "left_car")
        board.update_idletasks()
        board.after(50)

        # 4. Kiểm tra xem nước đi có hợp lệ không (luật cờ)
        if is_safe(path, next_row, col):
            # Nếu hợp lệ, đi sâu hơn (gọi đệ quy)
            solution_found = animate_backtracking_step(path + [col])

            # Nếu nhánh con tìm thấy lời giải (là goal), kết thúc
            if solution_found:
                return True

            # Nếu không, animation sẽ tự "quay lui" khi vòng lặp for
            # tiếp tục. Ta vẽ lại trạng thái cũ để xóa bước thử sai.
            drawcar(board, 0, 0, positions_to_draw, "red", "left_car")
            board.update_idletasks()
            board.after(50)

    # 5. Nếu thử hết các cột mà không có lựa chọn nào hợp lệ -> ngõ cụt
    return False

def draw_eliminations(board, positions):
    """Vẽ các dấu 'X' trên các ô bị loại bỏ."""
    board.delete("elimination_marker")
    for row, col in positions:
        x, y = col * SqSize + SqSize // 2, row * SqSize + SqSize // 2
        board.create_text(x, y, text="✕", font=("Arial", 20), fill="#555555", tags="elimination_marker")

def run_forward_checking():
    """Chuẩn bị và bắt đầu animation Forward Checking."""
    global confirmed_car, goal_map
    if not right_positions: 
        status_label.config(text="Lỗi: Hãy đặt goal ở bàn phải để so sánh!")
        return
    
    status_label.config(text="Forward Checking: Đang tìm goal...")
    confirmed_car = []
    goal_map = {r: c for r, c in sorted(right_positions)}
    
    # Khởi tạo "domain" (miền giá trị) cho mỗi dòng
    # Ban đầu, mỗi dòng đều có thể đặt ở tất cả các cột
    initial_domains = {r: list(range(SIZE)) for r in range(SIZE)}
    
    animate_forward_checking_step([], initial_domains)

def animate_forward_checking_step(path, domains):
    global after_id, left_positions

    # 1. Vẽ trạng thái hiện tại (không đổi)
    positions_to_draw = [(r, c) for r, c in enumerate(path)]
    left_positions = positions_to_draw
    drawcar(board, 0, 0, positions_to_draw, "red", "left_car")
    cost_value_label.config(text=str(len(path)))

    eliminated_pos = []
    for r in range(len(path), SIZE):
        for c in range(SIZE):
            if c not in domains[r]:
                eliminated_pos.append((r, c))
    draw_eliminations(board, eliminated_pos)
    board.update_idletasks()

    # 2. Điều kiện dừng (không đổi)
    if len(path) == SIZE:
        found_solution_map = {r: c for r, c in enumerate(path)}
        if found_solution_map == goal_map:
            status_label.config(text="Forward Checking: Đã tìm thấy goal!")
            return True
        else:
            return False

    # 3. Thử các lựa chọn cho dòng tiếp theo
    next_row = len(path)
    for col in domains[next_row]:
        board.after(100)

        # --- FORWARD CHECK (ĐÃ SỬA LỖI) ---
        new_domains = {r: list(d) for r, d in domains.items()}
        
        # Chỉ loại bỏ các ô trên cùng cột ở các dòng tương lai
        for r_future in range(next_row + 1, SIZE):
            if col in new_domains[r_future]:
                new_domains[r_future].remove(col)
        # --- KẾT THÚC SỬA LỖI ---

        is_dead_end = any(not new_domains[r] for r in range(next_row + 1, SIZE))
        
        if not is_dead_end:
            solution_found = animate_forward_checking_step(path + [col], new_domains)
            if solution_found:
                return True

    return False

def run_minimax():
    global confirmed_car, current_search_row, goal_map
    if not right_positions: 
        status_label.config(text="Lỗi: Hãy đặt quân xe ở bàn phải làm goal!")
        return
    
    confirmed_car, current_search_row = [], 0
    goal_map = {r: c for r, c in sorted(right_positions)}
    animate_minimax_step()

def minimax_evaluate(trial_col, target_col):
    return 10 if trial_col == target_col else -10

def animate_minimax_step():
    global after_id, current_search_row, confirmed_car, goal_map

    if len(confirmed_car) == len(goal_map): 
        status_label.config(text="Minimax: Đã hoàn thành!")
        return

    target_col = goal_map.get(current_search_row)
    

    best_move_for_max = -1
    max_score = -float('inf')
    
    # Dùng một danh sách để lên lịch animation
    cols_to_try = [c for c in range(SIZE) if c not in [pos[1] for pos in confirmed_car]]
    
    def try_next_col(index):
        global after_id
        nonlocal max_score, best_move_for_max
        if index >= len(cols_to_try):
            # Đã thử hết các cột, giờ chốt lựa chọn tốt nhất
            finalize_minimax_choice(best_move_for_max)
            return

        trial_col = cols_to_try[index]
        

        # Trực quan hóa bước "suy nghĩ"
        drawcar(board, 0, 0, confirmed_car, "red", "left_car")
        drawcar(board, 0, 0, [(current_search_row, trial_col)], "#007BFF", "minimax_try")
        board.update_idletasks()

# Min
        # Trong bài toán này, ta mô phỏng bằng hàm evaluate.
        score = minimax_evaluate(trial_col, target_col)
        
        # 3. MAX chọn nước đi cho điểm cao nhất
        if score > max_score:
            max_score = score
            best_move_for_max = trial_col
            cost_value_label.config(text=str(max_score)) # Hiển thị điểm tốt nhất tìm được

        # Lên lịch thử cột tiếp theo
        after_id = board.after(150, lambda: try_next_col(index + 1))
    
    # Bắt đầu thử từ cột đầu tiên
    try_next_col(0)

def finalize_minimax_choice(chosen_col):
    global after_id, current_search_row, confirmed_car
    
    board.delete("minimax_try")
    confirmed_car.append((current_search_row, chosen_col))
    current_search_row += 1
    
    drawcar(board, 0, 0, confirmed_car, "red", "left_car")
    cost_value_label.config(text="0") # Reset cost cho dòng mới
    board.update_idletasks()
    
    after_id = board.after(300, animate_minimax_step)

def run_ac3():
    """Chuẩn bị và bắt đầu animation AC-3."""
    global confirmed_car, goal_map
    if not right_positions: 
        status_label.config(text="Lỗi: Hãy đặt goal ở bàn phải để so sánh!")
        return
    
    status_label.config(text="AC-3: Đang tìm goal...")
    confirmed_car = []
    goal_map = {r: c for r, c in sorted(right_positions)}
    
    # Khởi tạo "domain" (miền giá trị) cho mỗi biến (hàng)
    initial_domains = {r: list(range(SIZE)) for r in range(SIZE)}
    
    # Bắt đầu với bàn cờ trống và domain đầy đủ
    animate_ac3_step([], initial_domains)

def animate_ac3_step(path, domains):
    global after_id, left_positions

    # --- Vẽ trạng thái hiện tại và các ô bị loại ---
    positions_to_draw = [(r, c) for r, c in enumerate(path)]
    left_positions = positions_to_draw
    drawcar(board, 0, 0, positions_to_draw, "red", "left_car")
    cost_value_label.config(text=str(len(path)))

    eliminated_pos = []
    for r in range(len(path), SIZE):
        for c in range(SIZE):
            if c not in domains[r]:
                eliminated_pos.append((r, c))
    draw_eliminations(board, eliminated_pos)
    board.update_idletasks()

    # --- Điều kiện dừng ---
    if len(path) == SIZE:
        if {r: c for r, c in enumerate(path)} == goal_map:
            status_label.config(text="AC-3: Đã tìm thấy goal!")
            return True
        return False

    # --- Thử các lựa chọn cho dòng tiếp theo ---
    next_row = len(path)
    for col in domains[next_row]:
        board.after(150)

        # --- LOGIC AC-3 ---
        # 1. Sao chép domain để không ảnh hưởng đến các nhánh khác
        new_domains = {r: list(d) for r, d in domains.items()}
        
        # 2. Tạo hàng đợi các "cung" (arc) cần kiểm tra.
        # Cung ở đây là ràng buộc giữa hàng vừa đặt (next_row) và các hàng tương lai.
        arc_queue = deque([(future_row, next_row) for future_row in range(next_row + 1, SIZE)])
        
        # 3. Xử lý hàng đợi để lan truyền ràng buộc
        while arc_queue:
            xi, xj = arc_queue.popleft() # Lấy ra một cung (hàng_tương_lai, hàng_hiện_tại)
            
            # Kiểm tra xem có giá trị nào trong domain của Xi
            # không thỏa mãn ràng buộc với giá trị vừa gán cho Xj (là `col`) không.
            # Ràng buộc ở đây là: giá trị cột không được trùng nhau.
            if col in new_domains[xi]:
                new_domains[xi].remove(col) # Nếu có, loại bỏ nó.

        # Kiểm tra xem có gây ra ngõ cụt không (domain rỗng)
        is_dead_end = any(not new_domains[r] for r in range(next_row + 1, SIZE))
        
        if not is_dead_end:
            solution_found = animate_ac3_step(path + [col], new_domains)
            if solution_found:
                return True

    return False

# Thao tác
def start():
    global after_id
    if after_id: board.after_cancel(after_id); after_id = None
    algo = algo_var.get()
    status_label.config(text=f"Đang chạy thuật toán {algo}...")
    board.delete("left_car"); left_positions.clear()
    
    if algo == "BFS": run_bfs() 
    elif algo == "DFS": run_dfs()
    elif algo == "UCS": run_ucs() # Gọi hàm UCS mới
    elif algo == "DLS": run_dls() # Gọi hàm DLS mới
    elif algo == "IDS": run_ids()
    elif algo == "A* Search": run_a_star()
    elif algo == "Greedy": run_greedy()
    elif algo == "Hill Climbing": hill_climbing(confirmed_car)
    elif algo == "Simulated Annealing": simulated_annealing()
    elif algo == "Genetic Algorithm": run_ga()
    elif algo == "Beam Search": beam_search()
    elif algo == "AndOr Search": run_andor()
    elif algo == "Belief State Search": run_beliefS()
    elif algo == "Back Tracking Search": run_backtracking()
    elif algo == "Forward Checking Search": run_forward_checking()
    elif algo == "Minimax": run_minimax()
    elif algo == "AC-3": run_ac3()

def stop():
    global after_id
    if after_id: board.after_cancel(after_id); after_id = None
    status_label.config(text="Đã dừng animation.")

def reset():
    stop() 
    status_label.config(text="Đã reset bàn cờ.")
    board.delete("all")
    chessboard(board, 0, 0); chessboard(board, start_x_right, 0)
    cost_value_label.config(text="0")
    algo_var.set("BFS")
    left_positions.clear(); right_positions.clear()
    confirmed_car.clear(); goal_map.clear()
    col_queue.clear(); col_stack.clear()

def restart():
    stop() 
    board.delete("left_car"); left_positions.clear()
    status_label.config(text="Đã restart bàn cờ bên trái.")

def choice():
    algo = algo_var.get()
    status_label.config(text=f"Đã chọn: {algo}")

def main():
    global board, status_label, cost_value_label, algo_var, start_x_right, left_positions, right_positions
    left_positions, right_positions = [], []
    game = tk.Tk(); game.title("Bài toán 8 quân hậu"); game.geometry("1200x700"); game.resizable(False, False)
    main_frame = tk.Frame(game); main_frame.pack(side=tk.LEFT, padx=10, pady=10)
    board_width = SIZE * SqSize * 2 + 50; board_height = SIZE * SqSize
    board = tk.Canvas(main_frame, width=board_width, height=board_height, bg="#f0f0f0"); board.pack()
    chessboard(board, 0, 0); start_x_right = SIZE * SqSize + 50; chessboard(board, start_x_right, 0)
    
    def on_click(event):
        x, y = event.x, event.y
        if start_x_right < x < (start_x_right + SIZE * SqSize):
            col = (x - start_x_right) // SqSize; row = y // SqSize; pos = (row, col)
            if pos in right_positions: right_positions.remove(pos); status_label.config(text="Đã xóa 1 quân xe.")
            else:
                is_row_occupied = any(r == row for r, c in right_positions)
                is_col_occupied = any(c == col for r, c in right_positions)
                if is_row_occupied or is_col_occupied: status_label.config(text="Vị trí không hợp lệ! Hàng/cột đã có xe.")
                else: right_positions.append(pos); status_label.config(text="Đặt quân xe ở bàn phải làm goal.")
            drawcar(board, start_x_right, 0, right_positions, color="red", tag="right_car")

    board.bind("<Button-1>", on_click)
    control_frame = tk.Frame(game, padx=10, pady=10); control_frame.pack(side=tk.RIGHT, fill="y")
    tk.Label(control_frame, text="Chọn thuật toán:", font=("Arial", 12, "bold")).pack(anchor="w")
    algo_var = tk.StringVar(value="BFS")
    
    algorithms = ["BFS", "DFS", "UCS", "DLS", "IDS", "A* Search", "Greedy", "Hill Climbing", "Simulated Annealing", "Genetic Algorithm", "Beam Search",
                  "AndOr Search", "Belief State Search", "Back Tracking Search", "Forward Checking Search", "Minimax", "AC-3"]
    for algo in algorithms:
        tk.Radiobutton(control_frame, text=algo, variable=algo_var, value=algo, command=choice).pack(anchor="w")

    tk.Label(control_frame, text="").pack()
    tk.Button(control_frame, text="Start", width=12, bg="#4CAF50", fg="white", command=start).pack(pady=5)
    tk.Button(control_frame, text="Stop", width=12, bg="#F44336", fg="white", command=stop).pack(pady=5)
    tk.Button(control_frame, text="Reset", width=12, bg="#2196F3", fg="white", command=reset).pack(pady=5)
    tk.Button(control_frame, text="Restart", width=12, bg="#FF9800", fg="white", command=restart).pack(pady=5)
    status_label = tk.Label(control_frame, text="Trạng thái: Đã sẵn sàng", font=("Arial", 10, "italic"), wraplength=150)
    status_label.pack(side=tk.BOTTOM, pady=10)
    cost_frame = tk.Frame(control_frame); cost_frame.pack(side=tk.BOTTOM, pady=(10, 5))
    tk.Label(cost_frame, text="Chi phí (Cost):", font=("Arial", 11, "bold")).pack()
    cost_value_label = tk.Label(cost_frame, text="0", font=("Consolas", 14, "bold"), fg="#333")
    cost_value_label.pack()

    game.mainloop()

if __name__ == "__main__":
    main()
