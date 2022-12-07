#!/usr/bin/env inlein

'{:dependencies [[org.clojure/clojure "1.8.0"]]}
(require '[clojure.set])

;;Part-I
;(defn find_duplicate_items_priority
;      [sack_string]
;      (def priority_map {"a" 1 "b" 2 "c" 3 "d" 4 "e" 5 "f" 6 "g" 7 "h" 8 "i" 9 "j" 10 "k" 11
;                         "l" 12 "m" 13 "n" 14 "o" 15 "p" 16 "q" 17 "r" 18 "s" 19 "t" 20 "u" 21
;                         "v" 22 "w" 23 "x" 24 "y" 25 "z" 26 "A" 27 "B" 28 "C" 29 "D" 30 "E" 31
;                         "F" 32 "G" 33 "H" 34 "I" 35 "J" 36 "K" 37 "L" 38 "M" 39 "N" 40 "O" 41
;                         "P" 42 "Q" 43 "R" 44 "S" 45 "T" 46 "U" 47 "V" 48 "W" 49 "X" 50 "Y" 51 "Z" 52})
;      (def first_item (subs sack_string 0 (/ (count sack_string) 2)))
;      ;(println first_item)
;      (def second_item (subs sack_string (/ (count sack_string) 2) (count sack_string)))
;      ;(println second_item)
;      (def f_set (set (seq first_item)))
;      (def s_set (set (seq second_item)))
;      (def comm_item (clojure.set/intersection f_set s_set))
;      ;(println "Common items: " (apply str comm_item))
;      (get priority_map (apply str comm_item))
;      )

;(def rucksack_items (clojure.string/split (slurp "items_rucksack.txt") #"\n"))
;(println (reduce + (map find_duplicate_items_priority rucksack_items)))

; Part-II
(defn find_duplicate_items_priority
      [group_items]
      (def priority_map {"a" 1 "b" 2 "c" 3 "d" 4 "e" 5 "f" 6 "g" 7 "h" 8 "i" 9 "j" 10 "k" 11
                         "l" 12 "m" 13 "n" 14 "o" 15 "p" 16 "q" 17 "r" 18 "s" 19 "t" 20 "u" 21
                         "v" 22 "w" 23 "x" 24 "y" 25 "z" 26 "A" 27 "B" 28 "C" 29 "D" 30 "E" 31
                         "F" 32 "G" 33 "H" 34 "I" 35 "J" 36 "K" 37 "L" 38 "M" 39 "N" 40 "O" 41
                         "P" 42 "Q" 43 "R" 44 "S" 45 "T" 46 "U" 47 "V" 48 "W" 49 "X" 50 "Y" 51 "Z" 52})

      (def f_set (set (seq (get group_items 0))))
      (def s_set (set (seq (get group_items 1))))
      (def t_set (set (seq (get group_items 2))))
      (def comm_item (clojure.set/intersection f_set s_set t_set))
      (println "Common item: " (apply str comm_item))
      (get priority_map (apply str comm_item))
      )

(def rucksack_items (clojure.string/split (slurp "items_rucksack.txt") #"\n"))

(loop [start 0
       end 3
       acc 0]
  (println "Current total priority: " acc)
  (if (> end (count rucksack_items))
      (println "goodbye..")
  (do (println (subvec rucksack_items start end))
      (println "Start: " start)
      (println "End: " end)
      (println "Current total priority: " acc)
      (recur (+ start 3) (+ end 3) (+ acc (find_duplicate_items_priority (subvec rucksack_items start end)))))))
