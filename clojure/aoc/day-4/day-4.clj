#!/usr/bin/env inlein

'{:dependencies [[org.clojure/clojure "1.8.0"]]}
; Part-I
;(defn check_contain
;      [input]
;      (println input)
;      ;(def pairs_in_ints (apply vector (map #(Integer/parseInt %)
;      ;                    (clojure.string/split
;      ;                      (clojure.string/join "-" (clojure.string/split input #",")) #"-"))))
;      (def pair_in_ints (apply vector (clojure.string/split (clojure.string/join "-" (clojure.string/split input #",")) #"-")))
;      ;["62" "97" "61" "61"]
;      (def pair (apply vector (map #(Integer/parseInt %) pair_in_ints)))
;      (def first_diff (- (get pair 0) (get pair 2)))
;      (def second_diff (- (get pair 1) (get pair 3)))
;      (if (<= (* first_diff second_diff) 0)
;            1
;            0)
;      )

; Part-II
(defn check_contain
      [input]
      (println input)
      ;(def pairs_in_ints (apply vector (map #(Integer/parseInt %)
      ;                    (clojure.string/split
      ;                      (clojure.string/join "-" (clojure.string/split input #",")) #"-"))))
      (def pair_in_ints (apply vector (clojure.string/split (clojure.string/join "-" (clojure.string/split input #",")) #"-")))
      ;["62" "97" "61" "61"]
      (def pair (apply vector (map #(Integer/parseInt %) pair_in_ints)))
      (def first_diff (- (get pair 0) (get pair 2)))
      (def second_diff (- (get pair 1) (get pair 3)))
      (def end_diff (- (get pair 3) (get pair 0)))
      (def beg_diff (- (get pair 2) (get pair 1)))
      (if (and (>= end_diff 0) (<= beg_diff 0))
            1
            0)
      )

(def assignments (clojure.string/split (slurp "assignment-ids.txt") #"\n"))
;(println assignments)
(map check_contain assignments)
