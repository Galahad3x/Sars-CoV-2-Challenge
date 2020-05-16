gap = 7
mismatch = [[0,2,3,4],[2,0,5,1],[3,5,0,1],[4,3,1,0]]

order :: Char -> Int
order 'A' = 0
order 'G' = 1
order 'C' = 2
order 'T' = 3

alignment_total :: String -> String -> ((String, String), Int)
alignment_total seq1 seq2 = ((trace_back (tracing score_matrix)),(last (last score_matrix)))
    where score_matrix = align seq1 seq2

tracing :: [[Int]] -> [String]
tracing scr_matrix = ["IEpale"]

align :: String -> String -> [[Int]]
align s1 s2 = align' [([0]++(take (length s1) [gap,gap*2..]))] 0 s1 s2

align' :: [[Int]] -> Int -> String -> String -> [[Int]]
align' current cont s1 s2 = if cont == (length s1) then current else align' (current ++ (new_row (last current) s1 s2 cont)) (cont+1) s1 s2

new_row :: [Int] -> String -> String -> Int -> [[Int]]
new_row last_row s1 s2 cont = [new_row' [(last_row!!0) + gap] last_row s1 s2 cont]

new_row' :: [Int] -> [Int] -> String -> String -> Int -> [Int]
new_row' current_row last_row@(l1:l2:ls) s1 s2 cont
    | ls == [] = current_row ++ [calculate_value (last current_row) l1 l2 (s1!!cont) (head s2)]
    | otherwise = new_row' (current_row ++ [calculate_value (last current_row) l1 l2 (s1!!cont) (head s2)]) (tail last_row) s1 (tail s2) (cont)

calculate_value :: Int -> Int -> Int -> Char -> Char -> Int
calculate_value left top_left top s1_c s2_c = minimum $ [left + gap, top + gap, top_left + (mismatch!!(order s1_c))!!(order s2_c)]

trace_back trbk = ("EEE","AAA")
