(ns rest-demo.core
  (:require [org.httpkit.server :as server]
            [compojure.core :refer :all]
            [compojure.route :as route]
            [ring.middleware.defaults :refer :all]
            [clojure.pprint :as pp]
            [clojure.string :as str]
            [clojure.data.json :as json])
  (:gen-class))

(defn hello_world_page
  [req]
  {:status 200
   :headers {"Content-Type" "text/html"}
   :body "Hello World..."})

(defn request_page
  [req]
  {:status 200
   :header {"Content-Type" "text/json"}
   :body (->> req
              (:params)
              (:id)
              (str/upper-case)
              (json/write-str)
              (str)
          )})

(defroutes app-routes
  (GET "/hello" [] hello_world_page)
  (GET "/hello/:id" [] request_page)
  (route/not-found "Error, page not found!"))

(defn -main
  "Entry point to the application"
  [& args]
  (let [port (Integer/parseInt (or (System/getenv "PORT") "3000"))]
    ; Run the server with Ring.defaults middleware
    (server/run-server (wrap-defaults #'app-routes site-defaults) {:port port})
    ; Run the server without ring defaults
    ;(server/run-server #'app-routes {:port port})
    (println (str "Running webserver at http:/127.0.0.1:" port "/"))))
