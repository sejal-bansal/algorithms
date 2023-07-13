package com.algorithms.array;

public class RemoveEvenInteger {

    public void printArray(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            System.out.println(arr[i] + " ");
        }
        System.out.println();
    }

    public int[] removeEven(int[] arr) {
        int oddCount = 0;
        for(int i = 0; i < arr.length; i++){
            if(arr[i] % 2 !=0){
                oddCount++;
            }
        }

        int[] result = new int[oddCount];
        int idx = 0;
        for(int i = 0; i < arr.length; i++){
            if(arr[i] % 2 !=0){
                result[idx] = arr[i];
                idx++;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        RemoveEvenInteger removeEvenInteger = new RemoveEvenInteger();
        int[] arr = {3, 2, 4, 7, 10, 6, 5};
//        removeEvenInteger.printArray(arr);
        int[] result = removeEvenInteger.removeEven(arr);
        removeEvenInteger.printArray(result);
        // Look into clas instances
    }
}
