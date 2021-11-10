package com.posco.sf.m00s22.p200.cm

import java.util.Properties
import com.posco.sf.m00s22.p200.DBProp

case class WBConfig(PATH:Option[String]){

  val WB_FILE = "WB.properties"
  val DB_FILE = "DB.properties"

  lazy val prop:Properties = loadProp()
  lazy val dbProp:Properties = loadDBProp()

  lazy val WORKCODE = prop.get("WORKCODE")
  lazy val MODE = prop.get("MODE")

  def getProperty(): Properties = prop
  def getDBProperty(): Properties = dbProp
  def getMode() =  MODE
  def getWorkcode() = WORKCODE

  // prop 정보 load
  private def loadProp():Properties = {
    val prop: Properties = new Properties()
    PATH match {
      case Some(p) =>
        prop.load(scala.io.Source.fromFile(p + "/" + WB_FILE, "utf-8").bufferedReader())
        println("load from : " + p + "/" + WB_FILE)
      case None =>
        prop.load(this.getClass.getResourceAsStream("/" + WB_FILE))
    }

    println("WBConfig : " + PATH.get + " -> MODE : " + prop.get("MODE") + ", WORKCODE : " + prop.get("WORKCODE"))
    prop
  }

  // DB prop 정보 load
  private def loadDBProp():Properties = {
    val prop: Properties = new Properties()
    prop.load(this.getClass.getResourceAsStream("/" + DB_FILE))
    prop
  }

  def getWBProp(): DBProp = {
    val id = "WB"
    val mode = MODE match {
      case "D" | "d" => "T" // 개발계
      case _ => ""
    }

    val workCode = WORKCODE match {
      case "k" | "K" => "K"
      case "p" | "P" => "P"
      case "c" | "C" => "C"
      case _ => ""
    }

    val DB_URL = s"$mode$workCode$id.URL"
    val DB_USER = s"$mode$workCode$id.USER"
    val DB_PWD = s"$mode$workCode$id.PWD"
    val DB_DRIVER = s"$mode$workCode$id.DRIVER"

    val prop = DBProp(dbProp.get(DB_URL).toString,
      {
        val prop = new Properties()
        prop.put("user", dbProp.get(DB_USER))
        prop.put("password", dbProp.get(DB_PWD))
        prop.put("driver", dbProp.get(DB_DRIVER))
        prop
      })
    prop
  }
}

object WBConfig {

  var config:WBConfig = null
  val SYS_CONFIG = "CONFIG_PATH"

  def getConfig(): WBConfig = {
    if(config == null) {
      val CONFIG = sys.props(SYS_CONFIG) match {
        case p:String => Some(p)
        case _ => Some("./conf")
      }
      config = WBConfig(CONFIG)
    }
    config
  }
}


