(ns tutorial.core
  (:gen-class)
  (:require [clojure.string :as str]))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println (str "Hello"))
  (println "Hello, World!")
  (str/reverse "hello")
  (println (str "Hello " args)))
