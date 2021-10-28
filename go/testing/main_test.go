package main

import (
	"testing"
)

var tests = []struct {
	name     string
	dividend float32
	divisor  float32
	expected float32
	isError  bool
}{
	{"valid-data", 100.0, 10.0, 10.0, false},
	{"invalid-data", 15.0, 0, 0, true},
	{"fraction", 15.0, 4, 3.75, false},
}

func TestDivision(t *testing.T) {
	for _, tt := range tests {
		got, err := divide(tt.dividend, tt.divisor)
		if tt.isError {
			if err == nil {
				t.Error("Expected an Error, but didn't get one")
			}
		} else {
			if err != nil {
				t.Error("Did not expect an Error, but got one")
			}
		}
		if got != tt.expected {
			t.Errorf("Expected %f, but got %f", tt.expected, got)
		}
	}
}
