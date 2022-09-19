(ns tutorial.functions
  (:gen-class))

;standard practice :-)
((defn helloworld
   "Prints hello world"
   []
   (println "Hello World...")))

; Lambdas
(def incrementor1 #(+ 1 %1))
(println (incrementor1 5))

(def incrementor2 (fn [x] (+ x 1)))
(println (incrementor2 4))

(def say_hello (fn [name] (println "Hello" name)))
(def say_bye (fn [name] (println "Good bye " name)))
(def greeting (fn [greetfunc name] (greetfunc name)))
(greeting say_hello "thosh")
(greeting say_bye "thosh")

(map inc (range 5))

;Closure
; increment maker
(defn inc-maker
  [inc-by]
  #(+ % inc-by))

; decrement maker
(defn dec-maker
  [dec-by]
  #(- % dec-by))
