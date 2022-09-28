(ns exercises.core)

;;Sum of the digits of a number

(defn inp
 []
 (println "Enter a number: ")
 (read-line))

(def number (inp))

(defn sum-digits
  [num]
  (reduce + (map #(Integer/parseInt (String/valueOf %)) (seq num))))

(sum-digits number)
