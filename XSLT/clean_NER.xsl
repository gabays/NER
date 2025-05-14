<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="xs" version="2.0">
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
    
    <xsl:strip-space elements="*"/>
    
    
    <!-- This XSL stylesheet is used to remove all tags enclosed between <p> and <l>. 
        The text is kept, only the tags are removed. -->
    <xsl:template match="node()|@*">
        <xsl:copy>
            <xsl:apply-templates select="node()|@*"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="tei:reg">
        <xsl:element name="reg" namespace="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="tei:FUNCTION">
        <xsl:element name="roleName" namespace="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="tei:EVENT">
        <xsl:element name="eventName" namespace="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="tei:PERSON">
        <xsl:element name="persName" namespace="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="tei:LOCATION">
        <xsl:element name="placeName" namespace="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="tei:ORGANIZATION">
        <xsl:element name="orgName" namespace="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
 
    <xsl:template match="tei:TIME">
        <xsl:element name="date" namespace="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="tei:PRODUCT">
        <xsl:element name="object" namespace="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
 
    <xsl:template match="tei:AMOUNT">
        <xsl:element name="measure" namespace="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

</xsl:stylesheet>