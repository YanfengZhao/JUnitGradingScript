//package testing;

import static org.junit.Assert.*;

import org.junit.Test;
import java.util.*;
import junit.framework.*;
import junit.framework.TestCase;

import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

public class SortTester{

	@Test 
    public void test1() {
        int[] arr = {-1, 5, 2, 1, 0, 8};
    	int[] expected = {-1, 0, 1, 2, 5, 8};
    	Sort.sort(arr);
    	assertArrayEquals(expected,arr);
    }

    @Test
    public void test2(){
    	int[] arr = {5, 5, 5};
    	int[] expected = {5, 5, 5};
    	Sort.sort(arr);
    	assertArrayEquals(expected,arr);
    }
    // public static void main(String args[]) {
    //     // String[] testCaseName = 
    //     //     { SortTester.class.getName() };
    //     // junit.swingui.TestRunner.main(testCaseName);
    //     //junit.textui.TestRunner.main(testCaseName);
    //     junit.textui.TestRunner.run(SortTester.class);
    // }
	public static void main(String[] args) {
    	Result result = JUnitCore.runClasses(SortTester.class);
        System.out.println("errorCount = " + result.getFailureCount());
    	for (Failure failure : result.getFailures()) {
      		System.out.println(failure.toString());
    	}
    	System.out.println(result.wasSuccessful());
        
  	}

}
