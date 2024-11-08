package com.example.bica
import utils.Feelings

import scala.collection.*

case class Actor(
  appraisal: Array[Float],
  feelings: Feelings,
  physState: mutable.Seq[PhysStateAtom],
)

