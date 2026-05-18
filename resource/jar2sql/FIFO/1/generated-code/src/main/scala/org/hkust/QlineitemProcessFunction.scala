import scala.math.Ordered.orderingToOrdered
import org.hkust.BasedProcessFunctions.RelationFKCoProcessFunction
import org.hkust.RelationType.Payload
import java.util.Date
import scala.util.matching.Regex
class QlineitemProcessFunction extends RelationFKCoProcessFunction[Any]("lineitem",1,Array("ORDERKEY"),Array("CUSTKEY"),true, true) {
override def isValid(value: Payload): Boolean = {
   if( (value("L_RETURNFLAG").asInstanceOf[String]=="R") ){
   true}else{
   false}
}
}
