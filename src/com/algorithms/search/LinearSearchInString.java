package com.algorithms.search;

import java.lang.reflect.Array;
import java.util.Arrays;

public class LinearSearchInString {
    public static void main(String[] args) {
        String name = "Sejal";
        char target = 'a';
        System.out.println(search2(name, target));
        System.out.println(Arrays.toString(name.toCharArray()));
    }

    static boolean search(String str, char target){
        if(str.length() == 0)
            return false;

        for(int i = 0; i < str.length(); i++){
            if(target == str.charAt(i))
                return true;
        }
        return false;
    }
    //implementation of for each in this function
    static boolean search2(String str, char target){
        if(str.length() == 0)
            return false;

        for(char ch : str.toCharArray()){
            if(ch == target)
                return true;
        }
        return false;
    }
}
