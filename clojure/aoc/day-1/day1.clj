#!/usr/bin/env inlein

'{:dependencies [[org.clojure/clojure "1.8.0"]]}

(defn string-to-sum
  [input]
  ;;(println "Called the function...")
  (def splitValuesinString (clojure.string/split input #"\n"))
  ;;(println splitValuesinString)
  (def valuesInInteger (map #(Integer/parseInt %) splitValuesinString))
  ;;(println valuesInInteger)
  (reduce + valuesInInteger)
  )

(def wholecontent (slurp "elves-calories.txt"))
(def splitIntoStrings (clojure.string/split wholecontent #"\n\n"))
;;(println "Total calories carried by each elf: " (map string-to-sum splitIntoStrings))
;;Part-1
(println "Part-1: Highest calories carried by an elf among all of them: " (apply max (map string-to-sum splitIntoStrings)))
;;Part-2
(println "Part-2: Total calories by top 3 carriers: " (reduce + (take 3 (sort (comp - compare) (map string-to-sum splitIntoStrings)))))