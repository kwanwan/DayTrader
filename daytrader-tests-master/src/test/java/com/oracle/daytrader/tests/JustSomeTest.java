package com.oracle.daytrader.tests;

import java.io.PrintStream;
import java.net.MalformedURLException;
import java.net.URL;

import org.junit.After;
import org.junit.Before;
import org.junit.FixMethodOrder;
import org.junit.Test;
import org.junit.runners.MethodSorters;

import net.sourceforge.jwebunit.junit.WebTester;
import net.sourceforge.jwebunit.util.TestContext;

@FixMethodOrder(MethodSorters.NAME_ASCENDING)
public class JustSomeTest {
	
	public static final String BASEURL_PROPERTYNAME = "com.oracle.daytrader.tests.baseurl";
	private WebTester delegate;
	private Reporter reporter;
	private TestContext testContext;
	
    @Before
    public void prepare() {
    	testContext = new TestContext();
    	
    	ensureProxyFromEnv(testContext);
    	
    	testContext.setBaseUrl(System.getProperty(BASEURL_PROPERTYNAME));

    	delegate = new WebTester();
    	delegate.setTestContext(testContext);
    	reporter = new Reporter();
    }
    @SuppressWarnings("unused")
	private TestContext ensureProxyFromProps(TestContext testContext) {
    	if (testContext == null) testContext = new TestContext();
    	
    	String proxyHost = System.getProperty("http.proxyHost");
    	int proxyPort = -1;
    	if (proxyHost!=null){
    		try{
    			proxyPort = Integer.parseInt(System.getProperty("http.proxyPort"));	
    		}catch(NumberFormatException nfe){
    			proxyPort = 80;
    		}
    	}
    	if (proxyHost!=null && proxyPort!=-1){
        	testContext.setProxyAuthorization(
        			/*user*/ null, /*passwd*/ null,
        			proxyHost, proxyPort);
    	}
    	return testContext;
    }
    @SuppressWarnings("unused")
	private TestContext ensureProxyFromEnv(TestContext testContext) {
    	if (testContext == null) testContext = new TestContext();
    	
    	String proxy = System.getenv("HTTP_PROXY");
        // we should get http://ch3-opc-proxy.usdc2.oraclecloud.com:80 for Chicago DC
    	URL proxyURL = null;
		try {
			proxyURL = new URL(proxy);
		} catch (MalformedURLException mue) {
			reporter.report(mue.getMessage());
		}
    	
    	if (proxyURL != null){
        	testContext.setProxyAuthorization(
        			/*user*/ null, /*passwd*/ null,
        			proxyURL.getHost(), proxyURL.getPort());
    	}
    	return testContext;
    }
    
    @After
    public void report(){
    	reporter = null;
    	delegate = null;
    }

	@Test
    public void test1Home() {
		try {
			reporter.notifyStart("Home");
			
			delegate.beginAt("contentHome.html");
			delegate.assertImagePresent("images/tradeOverview.png", null);
			
			reporter.notifyEnd();
			reporter.reportSuccess();
		} catch (AssertionError ae) {
			reporter.reportFailure(ae.getMessage());
			throw ae;
		}
    }	
	@Test
    public void test2Configuration() {
		try {
			reporter.notifyStart("Configuration");
			
			delegate.beginAt("config?action=resetTrade");
			delegate.assertTextPresent("Trade Reset completed successfully");
			
			delegate.gotoPage("config");
			delegate.setTextField("primIterations", "50");
			delegate.submit();
			delegate.assertTextPresent("DayTrader Configuration Updated");
			
			reporter.notifyEnd();
			reporter.reportSuccess();
		} catch (AssertionError ae) {
			reporter.reportFailure(ae.getMessage());
			throw ae;
		}
    }
	@Test
    public void test3Scenario() {
		try {
			reporter.notifyStart("Scenario");
			
			// start trading session
			delegate.beginAt("scenario");
			
			try{
				delegate.assertTextPresent("DayTrader Home");	
			} catch (AssertionError ae) {
				delegate.assertTextPresent("DayTrader Login");
				delegate.beginAt("config?action=buildDB");
				try {
					Thread.sleep(10000);
				} catch (InterruptedException ignored) {
				}
			}
			
			// buy some shares
			delegate.beginAt("scenario");
//			delegate.gotoPage("app?action=login&uid=uid=uid:0&passwd=xxx");
			delegate.gotoPage("app?action=quotes&symbols=s:0");
			delegate.submit("action");
			// check order is being processed
			delegate.assertTextPresent("New Order");
			// log off
			delegate.clickLinkWithExactText("Logoff");
			// log in
			delegate.submit();
			// check home page
			delegate.assertTextPresent("DayTrader Home");
			
			reporter.notifyEnd();
			reporter.reportSuccess();
		} catch (AssertionError ae) {
			reporter.reportFailure(ae.getMessage());
			throw ae;
		}
	}
	
	// Supporting classes
	
	public static class Reporter{
		private String testName;
		private long start;
		private long end;
		private PrintStream out;
		
		private Reporter(){
			notifyStart();
		}
		private Reporter(String testName){
			notifyStart(testName);
		}
		public void setTestName(String testName){
			this.testName = testName;
		} 
		public String getTestName(){
			return testName;
		} 
		public void setOut(PrintStream out) {
			this.out = out;
		}
		public PrintStream ensureOut() {
			return out!=null ? out : System.out;
		}
		public long nanosTaken(){
			return end - start;
		}
		public double millisTaken(){
			return ((double)(end - start))/(double) 1000000;
		}
		public double secondsTaken(){
			return ((double)(end - start))/(double) 1000000000;
		}
		public void notifyStart(String testName){
			setTestName(testName);
			notifyStart();
		}
		public void notifyStart(){
			this.start = System.nanoTime();
			this.end = this.start;
		}
		public void notifyEnd(){
			this.end = System.nanoTime();
		}
		public void reportSuccess(){
			ensureOut().println("Test " + getTestName() + " SUCCEEDED in " + secondsTaken() + " seconds");
		}
		public void reportFailure(String message){
			ensureOut().println("Test " + getTestName() + " FAILED in " + secondsTaken() + " seconds");
			ensureOut().println(message);
		}
		public void report(String message){
			ensureOut().println(message);
		}
	}
}
