(defproject aws-s3-demo "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}
  :dependencies [[org.clojure/clojure "1.10.3"]
                 [com.cognitect.aws/api "0.8.596"]
                 [com.cognitect.aws/endpoints "1.1.12.307"]
                 [com.cognitect.aws/s3 "822.2.1145.0"]
                 [com.cognitect.aws/lambda "822.2.1205.0"]
                 [com.cognitect.aws/dynamodb "825.2.1220.0"]]
  :main ^:skip-aot aws-s3-demo.core
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all
                       :jvm-opts ["-Dclojure.compiler.direct-linking=true"]}})
