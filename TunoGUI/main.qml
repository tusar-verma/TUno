import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

Window {
    id: window
    width: 900
    height: 500
    opacity: 1
    visible: true
    color: "#00000000"
    title: qsTr("Hello World")

    Rectangle {
        id: componentcontainer
        color: "#2e4061"
        border.color: "#18314f"
        border.width: 0
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        anchors.leftMargin: 0
        anchors.bottomMargin: 0
        anchors.topMargin: 0
    }
}


