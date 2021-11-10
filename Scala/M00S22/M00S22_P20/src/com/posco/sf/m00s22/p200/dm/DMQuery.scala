package com.posco.sf.m00s22.p200.dm

object DMQuery {

  val SCHEMA = ""

  def getDatasetQuery(queryId:String): String = {
    val SQL =
      s"""
          select m.mart_no, m.source_db_id as db_tp, m.table_nm as dataset_nm, m.query_text as sql
          from ${SCHEMA}VI_M00S22_DM_MART m
          where m.mart_no = ${queryId}
         """
    SQL
      }

  def getModelExQuery(mgmtId:String): String = {
    val SQL =
      s"""

         """
  }
}
