#!/usr/bin/env inlein

'{:dependencies [[org.clojure/clojure "1.8.0"]]}

;;Part-I
;(defn acc_points
;      [seed combo]
;      (def combinations {"AY" 8 "BZ" 9 "CX" 7 "AX" 4 "BY" 5 "CZ" 6 "AZ" 3 "BX" 1 "CY" 2})
;      ;;(println "Combo: " combo)
;      ;;(println "Points: " (get combinations combo))
;      (+ seed (get combinations combo))
;      )
;(def strategy (slurp "strategy-guide.txt"))
;(def combos (clojure.string/split strategy #"\n"))
;(def result (reduce acc_points 0 (map #(clojure.string/join (clojure.string/split % #" ")) combos )))
;(println result)

;;Part-II
(defn acc_points
      [seed combo]
      (def combinations {"AX" 3 "BX" 1 "CX" 2 "AY" 4 "BY" 5 "CY" 6 "AZ" 8 "BZ" 9 "CZ" 7})
      ;;(println "Combo: " combo)
      ;;(println "Points: " (get combinations combo))
      (+ seed (get combinations combo))
      )
(def strategy (slurp "strategy-guide.txt"))
(def combos (clojure.string/split strategy #"\n"))
(def result (reduce acc_points 0 (map #(clojure.string/join (clojure.string/split % #" ")) combos )))
(println result)
