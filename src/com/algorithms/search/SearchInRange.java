package com.algorithms.search;

public class SearchInRange {
    public static void main(String[] args) {
        int[] arr = {10, 20, 78, 98, 67, 56, 80};
        int target = 98;
        System.out.println(searchInRange(arr,1,4,target));
    }

    static int searchInRange(int[] arr, int start, int end, int target) {
        for (int i = start; i < end; i++) {
            int element = arr[i];
            if (element == target)
                return i;
        }
        return -1;

    }


}
