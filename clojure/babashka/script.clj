#!/bin/sh

#_(
   "exec" "bb" "$0" hello "$@"
   )

(require '[clojure.tools.cli :refer [parse-opts]])

(prn *command-line-args*)
(def cli-options
  ;; An option with a required argument
  [["-p" "--port PORT" "Port number"
    :default 80
    :parse-fn #(Integer/parseInt %)
    :validate [#(< 0 % 0x10000) "Must be a number between 0 and 65536"]]
   ["-h" "--help"]])

(parse-opts *command-line-args* cli-options)
