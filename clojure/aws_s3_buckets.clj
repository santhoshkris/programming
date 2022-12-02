#!/usr/bin/env inlein

'{:dependencies [[org.clojure/clojure "1.8.0"]
                 [amazonica "0.3.51"]]}

(require '[[amazonica.aws.s3 :as s3]
           [amazonica.aws.s3transfer :as s3t]])

(def bucket-name (first *command-line-args*))

(when-not bucket-name
  (println "Usage:" (System/getProperty "$0") "s3-bucket")
  (System/exit 1))

(defonce cred {:access-key "AKIAZA7VTYH5RDNDPDJN"
               :secret-key "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"
               :endpoint   "us-east-1"})

(defonce bucket "")
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
