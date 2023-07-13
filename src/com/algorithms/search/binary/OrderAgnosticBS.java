package com.algorithms.search.binary;

public class OrderAgnosticBS {
    public static void main(String[] args) {
        int[] arr = {90, 80, 75, 22, 11, 10, 5, 2, -3};
        int target = 11;
        int ans = orderAgnostic(arr, target);
        System.out.println(ans);
    }

    static int orderAgnostic(int[] arr, int target) {
        int start = 0;
        int end = arr.length - 1;

        //find whether the arr is sorted in ascending or descending order
        boolean isAsc = arr[start] < arr[end];
        while (start <= end) {
            int mid = start + (end - start) / 2;

            if (arr[mid] == target)
                return mid;

            if (isAsc) {
                if (target < arr[mid])
                    end = mid - 1;
                else
                    start = start + 1;
            } else {
                if (target > arr[mid])
                    end = mid - 1;
                else
                    start = start + 1;
            }
        }
        return -1;
    }
}
