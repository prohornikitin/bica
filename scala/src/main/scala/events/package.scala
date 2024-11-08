package com.example.bica

package object events {
    sealed trait Message
    case class DoAction(author: Actor, recipient: Actor, actionEffect: ActionEffect) extends Message
    case class OnActionReceived(author: Actor) extends Message
}
