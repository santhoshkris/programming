(ns aws-demo.core
  (:require [amazonica.aws.s3 :as s3]
            [amazonica.aws.s3transfer :as s3t])
  (:gen-class))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Hello, World!"))

(defonce cred {:access-key "AKIAYIVEVZR3YURUOPVE"
               :secret-key "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"
               :endpoint   "us-east-1"})

(defonce bucket "clojures3demo")
(defonce static-root "")

(defn create-bucket [nm]
  (s3/create-bucket cred nm))

(defn put-object [path]
  (let [content (clojure.java.io/file (str static-root path))]
    (if-not (.exists content)
      (println path "does not exist")
      (s3/put-object cred
                     :bucket-name bucket
                     :key path
                     :file content))))

(defn get-object [k]
  (s3/get-object cred
                 :bucket-name bucket
                 :key k))
