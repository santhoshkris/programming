package com.san.upgrad;

import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }
        partitionNegativeAndPositive(n, arr);
    }

    // Method to partition negative and positive numbers without comparing with 0
    static void partitionNegativeAndPositive(int n, int[] arr) {
        // Write your code here
        ArrayList<Integer> positives = new ArrayList();
        ArrayList<Integer> negatives = new ArrayList();
        ArrayList<Integer> others = new ArrayList<>();

        boolean flag = true;

        switch (Integer.signum(arr[0])) {
            case 0:
                flag = true;
                break;
            case 1:
                flag = true;
                break;
            case -1:
                flag = false;
        }

        for (int i = 0; i < n; i++) {
            switch (Integer.signum(arr[i])) {
                case 1:
                case 0:
                    positives.add(arr[i]);
                    break;
                case -1:
                    negatives.add(arr[i]);
                    break;
            }
        }

        if (flag) {
            if (positives.size() == 0)
                System.out.println("Array doesn't have positive numbers");
            else
                printNums(positives);
            if (negatives.size() == 0)
                System.out.println("Array doesn't have negative numbers");
            else
                printNums(negatives);
        } else {
            if (negatives.size() == 0)
                System.out.println("Array doesn't have negative numbers");
            else
                printNums(negatives);
            if (positives.size() == 0)
                System.out.println("Array doesn't have positive numbers");
            else
                printNums(positives);
        }
    }

    static void printNums(ArrayList<Integer> arr) {
        for (Integer i : arr) {
            System.out.printf("%d ", i);
        }
        System.out.println("");
    }
}
