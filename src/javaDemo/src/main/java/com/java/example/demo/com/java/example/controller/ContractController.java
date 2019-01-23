package com.java.example.demo.com.java.example.controller;

import com.java.example.demo.com.java.example.service.ContractService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.AutoConfigurationPackage;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author king
 * @version 1.0
 * @date 2018.11.28
 */
@AutoConfigurationPackage
@RestController
@RequestMapping(value="Contract", produces="application/json")
public class ContractController {
    private static Logger logger = LoggerFactory.getLogger(ContractController.class);

    /**
     * allTest
     */
    @RequestMapping(value = "/allTest", method = RequestMethod.GET)
    public String allTest() throws Exception{
        logger.info("ContractController allTest");
        StringBuffer stringBuffer = new StringBuffer();
        appendString(stringBuffer, "1. Test Function name start -------");
        appendString(stringBuffer, ContractService.nameTest());
        appendString(stringBuffer, "2. Test Function hello start -------");
        appendString(stringBuffer, ContractService.helloTest());
        appendString(stringBuffer, "3. Test Function testHello start -------");
        appendString(stringBuffer, ContractService.testHelloTest());
        appendString(stringBuffer, "4. Test Function testList start -------");
        appendString(stringBuffer,ContractService.testListTest());
        appendString(stringBuffer,"5. Test Function testListAndStr start -------");
        appendString(stringBuffer,ContractService.testListAndStrTest());
        appendString(stringBuffer,"6. Test Function testStructList start -------");
        appendString(stringBuffer,ContractService.testStructListTest());
        appendString(stringBuffer,"7. Test Function testStructListAndStr start -------");
        appendString(stringBuffer,ContractService.testStructListAndStrTest());
        appendString(stringBuffer,"8. Test Function testMap start -------");
        appendString(stringBuffer,ContractService.testMapTest());
        appendString(stringBuffer,"9. Test Function testGetMap start -------");
        appendString(stringBuffer,ContractService.testGetMapTest());
        appendString(stringBuffer,"10. Test Function testMapInMap start -------");
        appendString(stringBuffer,ContractService.testMapInMapTest());
        appendString(stringBuffer,"11. Test Function testMapInMap start -------");
        appendString(stringBuffer,ContractService.testGetMapInMapTest());
        appendString(stringBuffer,"12. Test Function testTransferMulti start -------");
        appendString(stringBuffer,ContractService.testTransferMultiTest());

        return stringBuffer.toString();
    }

    /**
     * deployContractTest
     */
    @RequestMapping(value = "/deployContractTest", method = RequestMethod.GET)
    public String deployContractTest() throws Exception{
        logger.info("ContractController deployContractTest");
        return ContractService.deployContractTest();
    }

    /**
     * helloTest
     */
    @RequestMapping(value = "/nameTest", method = RequestMethod.GET)
    public String nameTest() throws Exception{
        logger.info("ContractController nameTest");
        return ContractService.nameTest();
    }

    /**
     * helloTest
     */
    @RequestMapping(value = "/helloTest", method = RequestMethod.GET)
    public String helloTest() throws Exception{
        logger.info("ContractController helloTest");
        return ContractService.helloTest();
    }

    /**
     * testHelloTest
     */
    @RequestMapping(value = "/testHelloTest", method = RequestMethod.GET)
    public String testHelloTest() throws Exception{
        logger.info("ContractController testHelloTest");
        return ContractService.testHelloTest();
    }

    /**
     * testNumListTest
     */
    @RequestMapping(value = "/testNumListTest", method = RequestMethod.GET)
    public String testNumListTest() throws Exception{
        logger.info("ContractController testNumListTest");
        return ContractService.testListTest();
    }

    /**
     * testNumListAndStrTest
     */
    @RequestMapping(value = "/testNumListAndStrTest", method = RequestMethod.GET)
    public String testNumListAndStrTest() throws Exception{
        logger.info("ContractController testNumListAndStrTest");
        return ContractService.testListAndStrTest();
    }

    /**
     * testStructListTest
     */
    @RequestMapping(value = "/testStructListTest", method = RequestMethod.GET)
    public String testStructListTest() throws Exception{
        logger.info("ContractController testStructListTest");
        return ContractService.testStructListTest();
    }

    /**
     * testStructListAndStrTest
     */
    @RequestMapping(value = "/testStructListAndStrTest", method = RequestMethod.GET)
    public String testStructListAndStrTest() throws Exception{
        logger.info("ContractController testStructListAndStrTest");
        return ContractService.testStructListAndStrTest();
    }

    /**
     * testMapTest
     */
    @RequestMapping(value = "/testMapTest", method = RequestMethod.GET)
    public String testMapTest() throws Exception{
        logger.info("ContractController testMapTest");
        return ContractService.testMapTest();
    }

    /**
     * testGetMapTest
     */
    @RequestMapping(value = "/testGetMapTest", method = RequestMethod.GET)
    public String testGetMapTest() throws Exception{
        logger.info("ContractController testGetMapTest");
        return ContractService.testGetMapTest();
    }

    /**
     * testMapInMapTest
     */
    @RequestMapping(value = "/testMapInMapTest", method = RequestMethod.GET)
    public String testMapInMapTest() throws Exception{
        logger.info("ContractController testMapInMapTest");
        return ContractService.testMapInMapTest();
    }

    /**
     * testGetMapInMapTest
     */
    @RequestMapping(value = "/testGetMapInMapTest", method = RequestMethod.GET)
    public String testGetMapInMapTest() throws Exception{
        logger.info("ContractController testGetMapInMapTest");
        return ContractService.testGetMapInMapTest();
    }

    /**
     * testTransferMultiTest
     */
    @RequestMapping(value = "/testTransferMultiTest", method = RequestMethod.GET)
    public String testTransferMultiTest() throws Exception{
        logger.info("ContractController testTransferMultiTest");
        return ContractService.testTransferMultiTest();
    }
    
    private void appendString(StringBuffer stringBuffer, String string){
        stringBuffer.append(string).append("\r\n");
    }
}
