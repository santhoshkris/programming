(ns rest-api-tutorial.core
  (:gen-class)
  (:require [clj-http.client :as client]
            [cheshire.core :as json]))

(def book-url "https://the-one-api.dev/v2/book")
(def movie-url "https://the-one-api.dev/v2/movie")
(def characters-url "https://the-one-api.dev/v2/character?limit=50")

;; Generate the auth header map using the api token env variable
(def token-string (str "Bearer " (System/getenv "ONE_API_TOKEN")))
(def header-map (assoc-in {} [:headers :Authorization] token-string))

;; Get characters
(defn get-elf-characters
  [url]
  (let [resp (client/get url header-map)
        body-parsed (json/parse-string (:body resp) true)]
    (def elves (filter #(= (:race %) "Elf") (:docs body-parsed )))
    ;;(pprint elves)
    (println (str "Number of Elves we got : " (count elves)))
    (map #(:name %) elves)
    ))

;; Get movies
(defn get-movies
  [url]
  (let [resp (client/get url header-map)
        body (json/parse-string (:body resp) true)]
    (map #(:name %) (drop 2 (:docs body)))))

;; Get books
(defn get-books
  [url]
  (let [resp (client/get url)
        body (json/parse-string (:body resp) true)]
    (map #(:name %) (:docs body))))

(defn -main
  [arg]
  (case arg
    "books" (println (str "The books are: \n" (clojure.string/join "\n" (get-books book-url)) ))
    "movies" (println (str "The movies are: \n" (clojure.string/join "\n" (get-movies movie-url)) ))
    "elves" (println (str "The Elves are: \n" (clojure.string/join "\n" (get-elf-characters characters-url)) ))
    )
  )
