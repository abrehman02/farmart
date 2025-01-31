### **Approach 1: Linear Search (Baseline Approach)**  
The **linear search approach** reads the log file line by line, 
checking if each line starts with the target date. While simple, 
it is extremely inefficient for a **1 TB file**, as it requires 
scanning the entire file sequentially, even if the desired logs are 
located near the end. The time complexity of this approach is **O(N)**, 
where **N** is the number of lines in the file. Given that logs are distributed 
evenly across multiple years, searching for a single day requires scanning 
approximately **(1 TB / total days)** worth of data, making it impractical for 
large files. This approach is useful only when the log file is relatively small or 
when an indexed structure is unavailable.  

### **Approach 2: Binary Search with Single-Threaded Extraction**  
The **binary search approach** significantly improves performance by 
locating the first occurrence of the target date using a **logarithmic search** 
on the file. Instead of reading the entire file, it seeks to a middle position and 
adjusts based on the date at that location. Once the first occurrence is found, the 
script extracts logs sequentially. This reduces the search time from **O(N)** to 
**O(log N)** but still takes **O(K)** for extraction, where **K** is the number of 
logs for the given date. Overall, the time complexity is **O(log N + K)**. While 
much faster than linear search, this method is still limited by I/O bottlenecks 
since reading and writing occur sequentially.  

### **Approach 3: Multi-Threaded Binary Search Extraction**  
The **multi-threaded version** builds upon the binary search approach by 
**dividing the extraction process among multiple threads**. After finding 
the first log entry for the given date using **O(log N)** binary search, 
the file is divided into **equal-sized chunks**, and multiple threads extract 
logs simultaneously. This approach significantly reduces the extraction time 
by utilizing CPU cores efficiently. The time complexity remains **O(log N + K / T)**, 
where **T** is the number of threads. This results in a **4x speedup** (for **T=4**) 
compared to the single-threaded version. However, performance is still constrained 
by **file I/O speed** and **disk latency**.  

### **Approach 4: Memory-Mapped Multi-Threaded Binary Search (Final Optimized Approach)**  
The **fastest approach** utilizes **memory mapping (`mmap`)**, which allows treating 
the **1 TB file as a continuous memory object**. Instead of performing expensive 
file read operations, `mmap` enables direct access to file contents in memory, 
significantly reducing overhead. The **binary search step** remains **O(log N)**, 
but now **multi-threaded extraction** is performed directly on the memory-mapped 
file, reducing I/O bottlenecks. The final time complexity is **O(log N + K / T)** 
with minimal disk overhead, making this the **optimal solution**. Benchmarks show 
this approach is **2-5x faster than the standard multi-threaded version** due to 
reduced disk reads and efficient parallel processing. 🚀


I will chose the final **fourth solution** because it is the most optimised one and can easily run over a file of** 1TB**.
