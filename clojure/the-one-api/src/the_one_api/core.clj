(ns the-one-api.core
  (:gen-class)
  (:require [clj-http.client :as client]
            [cheshire.core :as json]))

(def book-url "https://the-one-api.dev/v2/book")
(def movie-url "https://the-one-api.dev/v2/movie")
(def characters-url "https://the-one-api.dev/v2/character?limit=50")

;;Interacting with The One API
;;
;; (defn one-api-fetch
;;   ([url auth]
;;    (if (= auth "yes")
;;      (let [resp (client/get url {:headers {:Authorization "Bearer c2j_HECs1xKCUJoG2aSi"}})
;;            body (json/parse-string (:body resp) true)]
;;        (map #(:name %) (:docs body)))
;;      (let [resp (client/get url)
;;            body (json/parse-string (:body resp) true)]
;;        (map #(:name %) (:docs body)))))

;;   ([url]
;;    (one-api-fetch url "no")))

;; Get characters
(defn get-elf-characters
  [url]
  (let [resp (client/get url {:headers {:Authorization "Bearer c2j_HECs1xKCUJoG2aSi"}})
        body-parsed (json/parse-string (:body resp) true)]
    (def elves (filter #(= (:race %) "Elf") (:docs body-parsed )))
    (map #(:name %) (:docs body))))

;; Get movies
(defn get-movies
  [url]
  (let [resp (client/get url {:headers {:Authorization "Bearer c2j_HECs1xKCUJoG2aSi"}})
        body (json/parse-string (:body resp) true)]
    (map #(println (:race %) (:name %)) (:docs body))))

;; Get books
(defn get-movies
  [url]
  (let [resp (client/get url {:headers {:Authorization "Bearer c2j_HECs1xKCUJoG2aSi"}})
        body (json/parse-string (:body resp) true)]
    (map #(:name %) (:docs body))))

(defn -main
  [arg]
  (if (= arg "books")
    (println (one-api-fetch book-url))
    (println (one-api-fetch movie-url "yes"))))
