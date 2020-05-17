import System.Environment
import System.IO

gap = 7
mismatch = [[0,2,3,4],[2,0,5,1],[3,5,0,1],[4,3,1,0]]

order :: Char -> Int
order 'A' = 0
order 'G' = 1
order 'C' = 2
order 'T' = 3
order x = 0

main = do
    userArgs <- getArgs
    handle1 <- openFile (userArgs!!0) ReadMode
    handle2 <- openFile (userArgs!!1) ReadMode
    contents1 <- hGetContents handle1
    contents2 <- hGetContents handle2
    print $ alignment_total (init contents1) (init contents2)

alignment_total :: String -> String -> ([String], Int)
alignment_total seq1 seq2 = (((tracing score_matrix)),(last (last score_matrix)))
    where score_matrix = align seq1 seq2

--alignment_total :: String -> String -> ((String, String), Int)
--alignment_total seq1 seq2 = ((trace_back (tracing score_matrix) seq1 seq2),(last (last score_matrix)))

tracing :: [[Int]] -> [String]
tracing scr_matrix = tracing' ([(['e']++(take (length (scr_matrix!!0) - 1) ['l','l'..]))]) scr_matrix 0

tracing' :: [String] -> [[Int]] -> Int -> [String]
tracing' current scr_mat counter = if (length current) == (length scr_mat) then current else tracing' (current ++ [(traced_row (scr_mat!!counter) (scr_mat!!(counter + 1)) ['u'] 0)]) (scr_mat) (counter + 1)

traced_row :: [Int] -> [Int] -> String -> Int -> String
traced_row top_num current_num current counter
    | (length current) == (length current_num) = current
    | otherwise = traced_row top_num current_num (current ++ [calc_trace (current_num!!counter) (top_num!!counter) (top_num!!(counter+1)) (current_num!!(counter+1))]) (counter+1)

calc_trace :: Int -> Int -> Int -> Int -> Char
calc_trace left top_left top res
    | res == (top + gap) = 'u'
    | res == (left + gap) = 'l'
    | otherwise = 'd'

align :: String -> String -> [[Int]]
align s1 s2 = align' [([0]++(take (length s2) [gap,gap*2..]))] 0 s1 s2

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

trace_back :: [String] -> String -> String -> (String, String)
trace_back trbk seq1 seq2 = trace_back' trbk seq1 seq2 "" ""

trace_back' :: [String] -> String -> String -> String -> String -> (String, String)
trace_back' trbk seq1 seq2 res1 res2
    | (last (last trbk)) == 'e' = (res1, res2)
    | (last (last trbk)) == 'd' = trace_back' (eliminate_both trbk) (init seq1) (init seq2) ((last seq1):res1) ((last seq2):res2)
    | (last (last trbk)) == 'l' = trace_back' (eliminate_last_each trbk) seq1 (init seq2) ('-':res1) ((last seq2):res2)
    | (last (last trbk)) == 'u' = trace_back' (eliminate_last trbk) (init seq1) seq2 ((last seq1):res1) ('-':res2)

eliminate_both :: [String] -> [String]
eliminate_both trbk = eliminate_last_each $ eliminate_last trbk

eliminate_last :: [String] -> [String]
eliminate_last trbk = (init trbk)

eliminate_last_each :: [String] -> [String]
eliminate_last_each trbk = map (init) trbk

