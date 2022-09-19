(ns tutorial.sequences
  (:gen-class))

(defn trymap
  [f coll]
  (map f coll))

(trymap inc [1 2 3 4])
(trymap #(* % %) [1 2 3 4])

; passing a collection of functions to map

(def sum #(reduce + %))

(def avg #(/ (sum %) (count %)))

(defn stats
  [coll]
  (map #(% coll) [sum count avg]))

; sum of the squares of the numbers
(reduce #(+ %1 (* %2 %2)) [1 2 3 4])

; reduce to create a new map from one with altered values
(reduce (fn [new-map [key val]]
          (assoc new-map key (inc val))) {} {:max 30 :min 10})

; reduce to filter out values from a map
(reduce (fn [new-map [key val]]
          (if (> val 4)
            (assoc new-map key val)
            new-map))
        {}
        {:human 4.1
         :critter 3.9})
