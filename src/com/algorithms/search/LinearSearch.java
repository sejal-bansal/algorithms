package com.algorithms.search;

import org.w3c.dom.css.ElementCSSInlineStyle;

//Serach in the array, if the element found, return the index of the target element
public class LinearSearch {
    public static void main(String[] args) {
        int[] nums = {10, 11, 67, 89, 3, -2, 45, 78, 99};
        int target = 45;
        int ans = linearSearch(nums,target);
        System.out.println(ans);

    }

    static int linearSearch(int[] arr, int target){
        if(arr.length == 0) { // check the edge case
            return -1;
        }
        //run the loop to find the target
        for(int index = 0; index < arr.length; index++){
            //check for element at every index if it is == target
            int element = arr[index];
            if(element == target)
                return index;
        }
        //this will execute if none of the above return statement returns any value
        return -1; // here we know that -1 can never be index, so the reason we are returning -1
    }

    static int linearSearchElement(int[] arr, int target){
        if(arr.length == 0) { // check the edge case
            return -1;
        }
        //run the loop to find the target
        for (int element : arr) {
            //check for element at every index if it is == target
            if (element == target)
                return element;
        }
        //this will execute if none of the above return statement returns any value
        return Integer.MAX_VALUE; //if you think that -1 element can be in the array, you can return this instead of -1
    }

}
