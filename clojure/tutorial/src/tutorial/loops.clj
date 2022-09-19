(ns tutorial.loops
  (:gen-class))

(defn loopOver
  [times]
  (loop [iteration 0]
    (println "Iteration: " iteration)
    (if (> iteration times)
      (println "Goodbye..!!")
      (recur (inc iteration)))))

; loop over a collection
(defn loopOverCollection
  [f coll]
  (println "Looping over collection...")
  (loop [remaining-coll coll
         result-set []]
    (if (empty? remaining-coll)
      result-set
      (let [[first & remaining] remaining-coll]
        (recur remaining (into result-set (vector (f first))))))))

(defn loopOverColl
  [f coll]
  (println "Looping over collection: ")
  (loop [remaining-coll coll
         result #{}]
    (if (empty? remaining-coll)
      result
      (let [[first & remaining ] remaining-coll]
        (recur remaining (into result (hash-set (f first))))))))

