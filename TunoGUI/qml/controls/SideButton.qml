import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
    id: btnSideMenu
    text: qsTr("Host game")
    property url btnIconSource: "../../Images/svg_images/home_icon.svg"
    property color colorDefault: "#2e3836"
    property color colorMouseOver: "#5f7470"
    property color colorPressed: "#a30000"
    property color leftSideDefaultColor: "#5f7470"
    property color leftSideActiveColor: "#a30000"
    property color rightSideActiveColor: "#121615"
    property int iconWidth: 18
    property int iconHeight: 18
    property bool active: false
    QtObject{
        id: internal

        property var dynamicColor: if(btnSideMenu.down){
                                       btnSideMenu.down ? colorPressed : colorDefault
                                   }else{
                                       btnSideMenu.hovered ? colorMouseOver : colorDefault
                                   }
    }

    implicitWidth: 250
    implicitHeight: 40
    background: Rectangle{
        id: bgBtn
        color: internal.dynamicColor

        Rectangle{
            id: leftSideRectangle
            anchors{
                top: parent.top
                left: parent.left
                bottom: parent.bottom
            }
            width: 3
            color: active ? leftSideActiveColor : leftSideDefaultColor
            visible: true
        }
        Rectangle{
            id: rightSideRectangle
            anchors{
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }
            width: 5
            color: active ? rightSideActiveColor : internal.dynamicColor
            visible: true
        }
    }

    contentItem: Item{
        id: content
        anchors.fill: parent
        ColorOverlay{
            anchors.fill: iconBtn
            source: iconBtn
            anchors.rightMargin: 0
            anchors.bottomMargin: 0
            anchors.leftMargin: 0
            anchors.topMargin: 0
            color: "#f5f5f5"
            antialiasing: true
            width: iconWidth
            height: iconHeight
        }

        Text {
            id: btnText
            text: btnSideMenu.text
            font: btnSideMenu.font
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 75
            color: "#f5f5f5"
            visible: true
        }

        Image{
            id: iconBtn
            source: btnIconSource
            anchors.leftMargin: 15
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            sourceSize.width: iconWidth
            sourceSize.height: iconHeight
            width: iconWidth
            height: iconHeight
            visible: false
            fillMode: Image.PreserveAspectFit
            antialiasing: true
        }
    }
}


/*##^##
Designer {
    D{i:0;formeditorZoom:1.66}
}
##^##*/
