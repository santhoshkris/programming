(ns aws-api-demo.core
  (:require [cognitect.aws.client.api :as aws]
            [cognitect.aws.credentials :as credentials])
  (:gen-class))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Hello, World!"))

(def s3 (aws/client {:api                  :s3
                     :region               "us-east-1"
                     :credentials-provider (credentials/basic-credentials-provider
                                            {:access-key-id     ""
                                             :secret-access-key ""})}))
(defn count-s3-buckets
  []
  (-> s3
      (aws/invoke {:op :ListBuckets})
      (:Buckets)
      (count)))

(defn list-s3-buckets
  []
  (-> s3
      (aws/invoke {:op :ListBuckets})
      (:Buckets)))

(defn create-s3-bucket
  [name]
  (-> s3
      (aws/invoke {:op :CreateBucket :request {:Bucket name}})))
