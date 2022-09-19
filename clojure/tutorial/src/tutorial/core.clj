(ns tutorial.core
  (:gen-class))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println (str "Hello"))
  (println "Hello, World!")
  (println (str "Hello " args)))
