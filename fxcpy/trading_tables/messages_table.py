from forexconnect import (
    IO2GMessageRow,
    IO2GMessagesTable,
    O2GTable
)


class MessagesTable(object):
    def __init__(self, table_manager):
        self._table_manager = table_manager
        self._set_table()
    
    def _set_table(self):        
        self._table = self._table_manager.getTable(O2GTable.Messages)
        self._table.__class__ = IO2GMessagesTable
        
    def _find_row(self, msg_id):
        row = self._table.findRow(msg_id)
        if row:
            row.__class__ = IO2GMessageRow
            row.release()
            return row

    def get_msg_id(self):
        """
        The unique identification number of the message.
        The number is unique within the same database that
        stores the account trader. For example, MINIDEMO or U100D1.
        The uniqueness of the message itself is assured by the
        combination of the database ID and the value of
        this field.
        
        Returns: string
        """
        msgs_dict = {}
        for i in range(self._table.size()):
            row = self._table.getRow(i)
            if row:
                row.__class__ = IO2GMessageRow
                msgs_dict[row.getMsgID()] = row.getTime()
                row.release()
        return msgs_dict
    
    def get_time(self, msg_id):
        """
        The date and time when the message is received.
        The time zone is defined by the system properties
        SERVER_TIME_UTCand BASE_TIME_ZONE.
        
        Returns: datetime
        """
        row = self._find_row(msg_id)
        if row:
            return row.getTime()

    def get_from(self, msg_id):
        """
        The login of the message sender.
        Returns: string
        """
        row = self._find_row(msg_id)
        if row:
            return row.getFrom()

    def get_type(self, msg_id):
        """
        The message container. It defines the way the message is
        displayed to the recipient in the FX Trading Station.
        The possible values are:
        0   Plain message that is displayed in the Messages window.
        1   Pop-up message that does not need to be answered.
        2   Pop-up message that needs to be answered.

        Returns: int
        """
        row = self._find_row(msg_id)
        if row:
            return row.getType()

    def get_feature(self, msg_id):
        """
        The type of the message content.
        The possible values are:
        1	Plain message.
        2	Trading hours.
        3	Questions.
        4	Information.
        5	Market conditions.
        6	Software updates.
        7	Emergency.
        8	System.

        Returns: string
        """
        row = self._find_row(msg_id)
        if row:
            return row.getFeature()
      
    def get_text(self, msg_id):
        """
        The text body of the message.
        
        Returns: string
        """
        row = self._find_row(msg_id)
        if row:
            return row.getText()

    def get_subject(self, msg_id):
        """
        The subject of the message.
        
        Returns: string
        """
        row = self._find_row(msg_id)
        if row:
            return row.getSubject()

    def get_html_fragment_flag(self, msg_id):
        """
        The HTML format flag. It defines whether the message is
        in the HTML format.
        The possible values are:
        TRUE	The message is in the HTML format.
        FALSE	The message is a plain text.

        Returns: boolean
        """
        row = self._find_row(msg_id)
        if row:
            return row.getHTMLFragmentFlag() 