package com.posco.sf.m00s22.p200.cm

import java.util.Properties
import java.sql.{Connection, DriverManager, ResultSet, ResultSetMetaData, Statement, SQLException}
import com.posco.sf.m00s22.p200.DBProp

object WBConnMgr {

  val MAS="MAS"
  val WB="WB"
  val M4A="M4A"
  val KUDU="KUDU"
  val M22="M22"
  val M30="M30"

  val config = WBConfig.getConfig()
  lazy val dbPropMap:Map[String, DBProp] = loadDBMap

  def getWBConn(): Connection = {
    getConn(WB)
  }

  def getDBProp(id:String): DBProp = {
    dbPropMap(id)
  }

  def getConn(id:String):Connection = {
    val prop = getDBProp(id)

    val jdbcDriver = prop.PROP.getProperty("driver")
    val userName = prop.PROP.getProperty("user")
    val password = prop.PROP.getProperty("password")
    val connectionUrl = prop.URL

    println(s"""getConn : $id -> $userName, $password, $connectionUrl""")

    Class.forName(jdbcDriver)
    DriverManager.getConnection(connectionUrl, userName, password)
  }

  def getDBProperty(id:String):Properties = {
    dbPropMap(id).PROP
  }

  private def loadDBMap():Map[String, DBProp] = {

    var result = Map[String, DBProp]()
    val SQL =
      s"""
          select serv_id, url, uid, pwd, driver
          from tb_m00s22_cm_server where serv_id = 'D';
         """

    val wbProp = config.getWBProp()
    val jdbcDriver = wbProp.PROP.getProperty("driver")
    val userName = wbProp.PROP.getProperty("user")
    val password = wbProp.PROP.getProperty("password")
    val connectionUrl = wbProp.URL

    Class.forName(jdbcDriver)
    val conn:Connection = DriverManager.getConnection(connectionUrl, userName, password)

    try {
      val stmt = conn.createStatement()
      val rs: ResultSet = stmt.executeQuery(SQL)

      while(rs.next()){
        val prop = new Properties()
        prop.put("user", rs.getString("uid"))
        prop.put("password", rs.getString("pwd"))
        prop.put("driver", rs.getString("driver"))

        val dbProp = new DBProp(rs.getString("url"), prop)
        result += (rs.getString("serv_id") -> dbProp)
      }

      // clean-up
      stmt.close
      conn.close
    } catch {
      case e: Exception => println(e);
    } finally {
      try {
        if (conn != null) conn.close
      } catch {
        case se: SQLException => se.printStackTrace
      }
    }
    result
  }
}
